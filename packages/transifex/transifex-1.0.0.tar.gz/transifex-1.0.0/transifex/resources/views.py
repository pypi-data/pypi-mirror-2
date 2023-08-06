# -*- coding: utf-8 -*-
from django.conf import settings
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.dispatch import Signal
from django.db.models import Count, Q, get_model
from django.http import (HttpResponseRedirect, HttpResponse, Http404, 
                         HttpResponseForbidden, HttpResponseBadRequest)
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.utils import simplejson
from django.utils.encoding import smart_unicode
from django.utils.translation import ugettext as _

from authority.views import permission_denied

from actionlog.models import action_logging
from transifex.resources.formats import get_i18n_handler_from_type
from transifex.languages.models import Language
from transifex.projects.models import Project
from transifex.projects.permissions import *
from transifex.projects.permissions.project import ProjectPermission
from transifex.projects.signals import post_resource_save, post_resource_delete
from transifex.teams.models import Team
from transifex.txcommon.decorators import one_perm_required_or_403
from transifex.txcommon.log import logger

from transifex.resources.forms import ResourceForm
from transifex.resources.models import Translation, Resource
from transifex.resources.stats import ResourceStatsList, ProjectStatsList
from transifex.resources.handlers import invalidate_stats_cache

from autofetch.forms import URLInfoForm
from autofetch.models import URLInfo

Lock = get_model('locks', 'Lock')

# Restrict access only for private projects 
# Allow even anonymous access on public projects
@one_perm_required_or_403(pr_project_private_perm,
    (Project, 'slug__exact', 'project_slug'), anonymous_access=True)
def resource_detail(request, project_slug, resource_slug):
    """
    Return the details overview of a project resource.
    """
    resource = get_object_or_404(Resource.objects.select_related(), project__slug = project_slug,
                                 slug = resource_slug)

    # We want the teams to check in which languages user is permitted to translate.
    user_teams = []
    if getattr(request, 'user') and request.user.is_authenticated():
        user_teams = Team.objects.filter(project=resource.project).filter(
            Q(coordinators=request.user)|
            Q(members=request.user)).distinct()

    statslist = ResourceStatsList(resource)

    return render_to_response("resources/resource_detail.html",
        { 'project' : resource.project,
          'resource' : resource,
          'languages' : Language.objects.order_by('name'),
          'user_teams' : user_teams,
          'statslist': statslist },
        context_instance = RequestContext(request))


@one_perm_required_or_403(pr_resource_delete,
                          (Project, "slug__exact", "project_slug"))
def resource_delete(request, project_slug, resource_slug):
    """
    Delete a Translation Resource in a specific project.
    """
    resource = get_object_or_404(Resource, project__slug = project_slug,
                                 slug = resource_slug)
    if request.method == 'POST':
        xhr = request.GET.has_key('xhr')
        
        import copy
        resource_ = copy.copy(resource)
        resource.delete()

        post_resource_delete.send(sender=None, instance=resource_,
            user=request.user)

        # Signal for logging
        request.user.message_set.create(
            message=_("The translation resource '%s' was deleted.") % resource_.name)

        invalidate_stats_cache(resource_)
        
        if xhr:
            response_dict = {'status': 200}
            return HttpResponse(simplejson.dumps(response_dict), mimetype='application/javascript')

        return HttpResponseRedirect(reverse('project_detail',
                                    args=[resource.project.slug]),)
    else:
        return render_to_response(
            'resources/resource_confirm_delete.html', {'resource': resource,},
            context_instance=RequestContext(request))



@one_perm_required_or_403(pr_resource_add_change,
                          (Project, "slug__exact", "project_slug"))
def resource_edit(request, project_slug, resource_slug):
    """
    Edit the metadata of  a Translation Resource in a specific project.
    """
    resource = get_object_or_404(Resource, project__slug = project_slug,
                                  slug = resource_slug)
    try:
        urlinfo = URLInfo.objects.get(resource = resource)
    except URLInfo.DoesNotExist:
        urlinfo = None

    if request.method == 'POST':
        resource_form = ResourceForm(request.POST, instance=resource,)
        if urlinfo:
            url_form = URLInfoForm(request.POST, instance=urlinfo,)
        else:
            url_form = URLInfoForm(request.POST,)
        if resource_form.is_valid() and url_form.is_valid():
            urlinfo = url_form.save(commit=False)
            resource_new = resource_form.save()
            urlinfo.resource = resource_new
            try:
                urlinfo.update_source_file(fake=True)
            except Exception, e:
                url_form._errors['source_file_url'] = _("The URL you provided"
                    " doesn't link to valid file.")
                return render_to_response('resources/resource_form.html', {
                    'resource_form': resource_form,
                    'url_form': url_form,
                    'resource': resource,
                }, context_instance=RequestContext(request))

            urlinfo.save()

            post_resource_save.send(sender=None, instance=resource_new,
                created=False, user=request.user)

            return HttpResponseRedirect(reverse('resource_detail',
                args=[resource.project.slug, resource.slug]))
    else:
        if resource:
            initial_data = {}

        if urlinfo:
            url_form = URLInfoForm(instance=urlinfo,)
        else:
            url_form = URLInfoForm()
        resource_form = ResourceForm(instance=resource)

    return render_to_response('resources/resource_form.html', {
        'resource_form': resource_form,
        'url_form': url_form,
        'resource': resource,
    }, context_instance=RequestContext(request))


# Restrict access only for private projects 
# Allow even anonymous access on public projects
@one_perm_required_or_403(pr_project_private_perm,
    (Project, 'slug__exact', 'project_slug'), anonymous_access=True)
def resource_actions(request, project_slug=None, resource_slug=None,
                     target_lang_code=None):
    """
    Ajax view that returns an fancybox template snippet for resource specific 
    actions.
    """
    resource = get_object_or_404(Resource, project__slug = project_slug,
                                 slug = resource_slug)
    target_language = get_object_or_404(Language, code=target_lang_code)
    project = resource.project
    # Get the team if exists to use it for permissions and links
    team = Team.objects.get_or_none(project, target_lang_code)

    disabled_languages_ids = Translation.objects.filter(
        source_entity__resource = resource).values_list(
            'language', flat=True).distinct()
    languages = Language.objects.filter()

    lock = Lock.objects.get_valid(resource, target_language)

    # We want the teams to check in which languages user is permitted to translate.
    user_teams = []
    if getattr(request, 'user') and request.user.is_authenticated():
        user_teams = Team.objects.filter(project=resource.project).filter(
            Q(coordinators=request.user)|
            Q(members=request.user)).distinct()

    statslist = ResourceStatsList(resource)
    #FIXME: Wordcount is expensive and isn't being cached
    # Find a way to handle this before enabling it
    wordcount = statslist.wordcount
    stats = statslist.stat(target_language)

    return render_to_response("resources/resource_actions.html",
    { 'project' : project,
      'resource' : resource,
      'target_language' : target_language,
      'team' : team,
      'languages': languages,
      'disabled_languages_ids': disabled_languages_ids,
      'lock': lock,
      'user_teams': user_teams,
      'stats': stats,
      'wordcount': wordcount,
      },
    context_instance = RequestContext(request))


# Restrict access only for private projects 
# Allow even anonymous access on public projects
@one_perm_required_or_403(pr_project_private_perm,
    (Project, 'slug__exact', 'project_slug'), anonymous_access=True)
def project_resources(request, project_slug=None, offset=None, **kwargs):
    """
    Ajax view that returns a table snippet for all the resources in a project.
    
    If offset is provided, then the returned table snippet includes only the
    rows beginning from the offset and on.
    """
    more = kwargs.get('more', False)
    MORE_ENTRIES = 5
    project = get_object_or_404(Project, slug=project_slug)
    total = Resource.objects.filter(project=project).count()
    begin = int(offset)
    end_index = (begin + MORE_ENTRIES)
    resources = Resource.objects.filter(project=project)[begin:]
    # Get the slice :)
    if more and (not end_index >= total):
        resources = resources[begin:end_index]

    statslist = ProjectStatsList(project)

    return render_to_response("resources/resource_list_more.html", { 
        'project': project,
        'statslist': statslist},
        context_instance = RequestContext(request))


# Restrict access only to : (The checks are done in the view's body)
# 1)those belonging to the specific language team (coordinators or members)
# 2)project maintainers
# 3)global submitters (perms given through access control tab)
# 4)superusers
@login_required
def clone_language(request, project_slug=None, resource_slug=None,
            source_lang_code=None, target_lang_code=None):
    '''
    Get a resource, a src lang and a target lang and clone all translation
    strings for the src to the target.

    The user is redirected to the online editor for the target language.
    '''

    resource = get_object_or_404(Resource, slug=resource_slug,
                                 project__slug=project_slug)

    # Permissions handling
    # Project should always be available
    project = get_object_or_404(Project, slug=project_slug)
    team = Team.objects.get_or_none(project, target_lang_code)
    check = ProjectPermission(request.user)
    if not check.submit_translations(team or project) or not \
        resource.accept_translations:
        return permission_denied(request)

    source_lang = get_object_or_404(Language, code=source_lang_code)
    target_lang = get_object_or_404(Language, code=target_lang_code)

    # get the strings which will be cloned
    strings = Translation.objects.filter(
                source_entity__resource = resource,
                language = source_lang)

    # If the language we want to create, has the same plural rules with the 
    # source, we also copy the pluralized translations!
    if not source_lang.get_pluralrules() == target_lang.get_pluralrules():
        strings = strings.exclude(source_entity__pluralized = True)

    # clone them in new translation
    for s in strings:
        Translation.objects.get_or_create(
                    language = target_lang,
                    string = s.string,
                    source_entity = s.source_entity,
                    rule = s.rule)

    invalidate_stats_cache(resource, target_lang)
    return HttpResponseRedirect(reverse('translate_resource', args=[project_slug,
                                resource_slug, target_lang_code]),)


# Restrict access only to maintainers of the projects.
@one_perm_required_or_403(pr_resource_translations_delete,
                          (Project, "slug__exact", "project_slug"))
def resource_translations_delete(request, project_slug, resource_slug, lang_code):
    """
    Delete the set of Translation objects for a specific Language in a Resource.
    """
    resource = get_object_or_404(Resource, project__slug = project_slug,
                                 slug = resource_slug)

    language = get_object_or_404(Language, code=lang_code)

    # Use a flag to denote if there is an attempt to delete the source language.
    is_source_language = False
    if resource.source_language == language:
        is_source_language = True

    if request.method == 'POST':
        Translation.objects.filter(source_entity__resource=resource, 
            language=language).delete()

        request.user.message_set.create(
            message=_("The translations of language %(lang)s for the resource "
                      "%(resource)s were deleted successfully.") % {
                          'lang': language.name,
                          'resource': resource.name})
        invalidate_stats_cache(resource, language)
        return HttpResponseRedirect(reverse('resource_detail',
                                    args=[resource.project.slug, resource.slug]),)
    else:
        return render_to_response(
            'resources/resource_translations_confirm_delete.html',
            {'resource': resource,
             'language': language,
             'is_source_language': is_source_language},
            context_instance=RequestContext(request))


def _compile_translation_template(resource=None, language=None):
    """
    Given a resource and a language we create the translation file
    """
    parser = get_i18n_handler_from_type(resource.i18n_type)
    handler = parser(resource = resource, language = language)
    handler.compile()

    return handler.compiled_template


# Restrict access only for private projects 
# DONT allow anonymous access
@login_required
@one_perm_required_or_403(pr_project_private_perm,
    (Project, 'slug__exact', 'project_slug'))
def get_translation_file(request, project_slug, resource_slug, lang_code):
    """
    View to export all translations of a resource for the requested language
    and give the translation file back to the user.
    """

    resource = get_object_or_404(Resource, project__slug = project_slug,
        slug = resource_slug)

    language = get_object_or_404(Language, code=lang_code)

    try:
        template = _compile_translation_template(resource, language)
    except Exception, e:
        request.user.message_set.create(message=_("Error compiling translation file."))
        logger.error("Error compiling '%s' file for '%s': %s" % (language, 
            resource, str(e)))
        return HttpResponseRedirect(reverse('resource_detail',
            args=[resource.project.slug, resource.slug]),)

    i18n_method = settings.I18N_METHODS[resource.i18n_type]
    response = HttpResponse(template,
        mimetype=i18n_method['mimetype'])
    response['Content-Disposition'] = ('attachment; filename="%s_%s%s"' % (
        smart_unicode(resource.name), language.code,
        i18n_method['file-extensions'].split(', ')[0]))

    return response

# Restrict access only to : (The checks are done in the view's body)
# 1)those belonging to the specific language team (coordinators or members)
# 2)project maintainers
# 3)global submitters (perms given through access control tab)
# 4)superusers
@login_required
def lock_and_get_translation_file(request, project_slug, resource_slug, lang_code):
    """
    Lock and download the translations file.
    
    View to lock a resource for the requested language and as a second step to 
    download (export+download) the translations in a formatted file.
    """

    resource = get_object_or_404(Resource, project__slug = project_slug,
        slug = resource_slug)

    # Permissions handling
    # Project should always be available
    project = get_object_or_404(Project, slug=project_slug)
    team = Team.objects.get_or_none(project, lang_code)
    check = ProjectPermission(request.user)
    if not check.submit_translations(team or project) or not \
        resource.accept_translations:
        return permission_denied(request)

    language = get_object_or_404(Language, code=lang_code)
    lock = Lock.objects.get_valid(resource, language)
    can_lock = Lock.can_lock(resource, language, request.user)
    response = {}

    if not can_lock:
        #print_gray_text(You cannot assign this file to you)
        response['status'] = "FAILED"
        response['message'] = _("Sorry, you cannot assign this file to you!")
    else:
        # User can lock
        if not lock:
            try:
                # Lock the resource now
                Lock.objects.create_update(resource, language, request.user)
                response['status'] = 'OK'
                response['redirect'] = reverse('download_translation',
                    args=[resource.project.slug, resource.slug, lang_code])
            except:
                response['status'] = "FAILED"
                response['message'] = _("Failed to lock the resource!")
        else:
            if lock.owner == request.user:
                try:
                    # File already locked by me, so extend the lock period.
                    Lock.objects.create_update(resource, language, request.user)
                    response['status'] = 'OK'
                    response['redirect'] = reverse('download_translation',
                        args=[resource.project.slug, resource.slug, lang_code])
                except:
                    response['status'] = "FAILED"
                    response['message'] = _("Failed to extend lock period on "
                                            "the resource!")
            else:
                # File locked by someone else:
                response['status'] = "FAILED"
                response['message'] = _("You cannot lock it right now! ( Locked "
                                        "by %s )" % (lock.owner,))

    return HttpResponse(simplejson.dumps(response), mimetype='application/json')

