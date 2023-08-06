# -*- coding: utf-8 -*-
import os
from datetime import datetime
import markdown

from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from django.db import models, IntegrityError
from django.db.models import permalink
from django.dispatch import Signal
from django.forms import ModelForm
from django.contrib.auth.models import User
from django.contrib.contenttypes import generic
from django.contrib.contenttypes.models import ContentType
from django.utils.html import escape

from authority.models import Permission
from notification.models import ObservedItem
import tagging
from tagging.fields import TagField

from codebases.models import Unit
from vcs.models import VcsUnit
from tarball.models import Tarball
from translations.models import POFile
from txcommon.log import logger, log_model
from txcommon.notifications import is_watched_by_user_signal
from projects.handlers import get_trans_handler
from projects import signals

def cached_property(func):
    """
    Cached property.

    This function is able to verify if an instance of a property field
    was already created before and, if not, it creates the new one.
    When needed it also is able to delete the cached property field from
    the memory.

    Usage:
    @cached_property
    def trans(self):
        ...

    del(self.trans)

    """
    def _set_cache(self):
        cache_attr = "__%s" % func.__name__
        try:
            return getattr(self, cache_attr)
        except AttributeError:
            value = func(self)
            setattr(self, cache_attr, value)
            return value

    def _del_cache(self):
        cache_attr = "__%s" % func.__name__
        try:
            delattr(self, cache_attr)
        except AttributeError:
            pass

    return property(_set_cache, fdel=_del_cache)


class DefaultProjectManager(models.Manager):
    """
    This is the defautl manager of the project model (asigned to objects field).
    """

    def watched_by(self, user):
        """
        Retrieve projects being watched by the specific user.
        """
        try:
            ct = ContentType.objects.get(name="project")
        except ContentType.DoesNotExist:
            pass
        observed_projects = [i[0] for i in list(set(ObservedItem.objects.filter(user=user, content_type=ct).values_list("object_id")))]
        watched_projects = []
        for object_id in observed_projects:
            try:
                watched_projects.append(Project.objects.get(id=object_id))
            except Project.DoesNotExist:
                pass
        return watched_projects

    def maintained_by(self,user):
        """
        Retrieve projects being maintained by the specific user.
        """
        return Project.objects.filter(maintainers__id=user.id)

    def translated_by(self, user):
        """
        Retrieve projects being translated by the specific user.
        
        The method returns all the projects in which user has been granted 
        permissions to submit translations.
        """
        try:
            ct = ContentType.objects.get(name="project")
        except ContentType.DoesNotExist:
            pass
        return Permission.objects.filter(user=user, content_type=ct, approved=True)
    

class PublicProjectManager(models.Manager):
    """
    Return a QuerySet of public projects.
    
    Usage: Projects.public.all()
    """

    def get_query_set(self):
        return super(PublicProjectManager, self).get_query_set().filter(private=False)

    def recent(self):
        return self.order_by('-created')

    def open_translations(self):
        return self.filter(component__allows_submission=True).distinct()


class Project(models.Model):

    """
    A project is a group of translatable resources.

    >>> p, created = Project.objects.get_or_create(slug="foo", name="Foo Project")
    >>> p = Project.objects.get(slug='foo')
    >>> p
    <Project: Foo Project>
    >>> Project.objects.create(slug="foo", name="Foo Project")
    Traceback (most recent call last):
        ...
    IntegrityError: column slug is not unique
    >>> if created: p.delete()

    """

    private = models.BooleanField(default=False, verbose_name=_('Private'),
        help_text=_('A private project is visible only by you and your team.'
                    'Moreover, private projects are limited according to billing'
                    'plans for the user account.'))
    slug = models.SlugField(_('Slug'), max_length=30, unique=True,
        help_text=_('A short label to be used in the URL, containing only '
                    'letters, numbers, underscores or hyphens.'))
    name = models.CharField(_('Name'), max_length=50,
        help_text=_('A short name or very short description.'))
    description = models.CharField(_('Description'), blank=True, max_length=255,
        help_text=_('A sentence or two describing the object (optional).'))
    long_description = models.TextField(_('Long description'), blank=True, 
        max_length=1000,
        help_text=_('A longer description (optional). Use Markdown syntax.'))
    homepage = models.URLField(_('Homepage'), blank=True, verify_exists=False)
    feed = models.CharField(_('Feed'), blank=True, max_length=255,
        help_text=_('An RSS feed with updates to the project.'))
    bug_tracker = models.URLField(_('Bug tracker'), blank=True,
        help_text=_('The URL for the bug and tickets tracking system '
                    '(Bugzilla, Trac, etc.)'))
    anyone_submit = models.BooleanField(_('Anyone can submit'), 
        default=False, blank=False,
        help_text=_('Can anyone submit files to this project?'))

    hidden = models.BooleanField(_('Hidden'), default=False, editable=False,
        help_text=_('Hide this object from the list view?'))
    enabled = models.BooleanField(_('Enabled'),default=True, editable=False,
        help_text=_('Enable this object or disable its use?'))
    created = models.DateTimeField(auto_now_add=True, editable=False)
    modified = models.DateTimeField(auto_now=True, editable=False)

    tags = TagField(verbose_name=_('Tags'))

    # Relations
    maintainers = models.ManyToManyField(User, verbose_name=_('Maintainers'),
        related_name='projects_maintaining', blank=False, null=True)

    outsource = models.ForeignKey('Project', blank=True, null=True,
        verbose_name=_('Outsource project'),
        help_text=_('Project that owns the access control of this project.'))

    owner = models.ForeignKey(User, blank=True, null=True,
        editable=False, verbose_name=_('Owner'),
        help_text=_('The user who owns this project.'))

    # Normalized fields
    long_description_html = models.TextField(_('HTML Description'), blank=True, 
        max_length=1000,
        help_text=_('Description in HTML.'), editable=False)

    # Managers
    objects = DefaultProjectManager()
    public = PublicProjectManager()

    def __unicode__(self):
        return self.name

    def __repr__(self):
        return _('<Project: %s>') % self.name

    class Meta:
        verbose_name = _('project')
        verbose_name_plural = _('projects')
        db_table  = 'projects_project'
        ordering  = ('name',)
        get_latest_by = 'created'

    def save(self, *args, **kwargs):
        """Save the object in the database."""
        long_desc = escape(self.long_description)
        self.long_description_html = markdown.markdown(long_desc)
        super(Project, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        for c in Component.objects.filter(project=self):
            c.delete()
        super(Project, self).delete(*args, **kwargs)

    @permalink
    def get_absolute_url(self):
        return ('project_detail', None, { 'project_slug': self.slug })

    def is_watched_by(self, user, signal=None):
        return is_watched_by_user_signal(self, user, signal)

    @property
    def blacklist_vcsunits(self):
        """Return all the vcsunits that arent allowed to be used."""
        return VcsUnit.objects.exclude(
            component__id__in=self.component_set.all().values('id'))

tagging.register(Project, tag_descriptor_attr='tagsobj')
log_model(Project)


class ComponentManager(models.Manager):

    def with_language(self, language):
        """
        Return distinct components which ship a language's files.

        Poll Components for ones that have files of a particular
        language. Can be used by a language page, to list all
        components which ship this language.
        """

        pofiles = POFile.objects.filter(language=language)
        qs = self.filter(id__in=[c.object_id for c in pofiles])
        return qs.distinct()

    def untranslated_by_lang_release(self, language, release):
        """
        Return a QuerySet of components without translations for a specificity
        language and release.
        """
        comp_query = release.components.values('pk').query
        ctype = ContentType.objects.get_for_model(Component)
        po = POFile.objects.filter(content_type=ctype,
                                   object_id__in=comp_query,
                                   language__id=language.id)
        poc = po.values('object_id').query
        return Component.objects.exclude(pk__in=poc).filter(
                            releases__pk=release.pk).order_by('project__name',
                                                              'name')


class Component(models.Model):

    """A component is a translatable resource."""

    slug = models.SlugField(_('Slug'), max_length=30,
        help_text=_('A short label to be used in the URL, containing only '
                    'letters, numbers, underscores or hyphens.'))
    name = models.CharField(_('Name'), max_length=50,
        help_text=_('A short name or very short description.'))
    description = models.CharField(_('Description'), blank=True, max_length=255,
        help_text=_('A sentence or two describing the object (optional).'))
    long_description = models.TextField(_('Long description'), blank=True, 
        max_length=1000,
        help_text=_('A longer description (optional). Use Markdown syntax.'))
    source_lang = models.CharField(_('Source language'), max_length=50,
        help_text=_("The source language for this component "
                    "(e.g., 'en', 'pt_BR', 'el')."))
    i18n_type = models.CharField(_('I18n type'), max_length=20,
        choices=settings.TRANS_CHOICES.items(),
        help_text=_("The type of i18n support for the source code (%s)" %
                    ', '.join(settings.TRANS_CHOICES.keys())))
    file_filter = models.CharField(_('File filter'), max_length=50,
        help_text=_("A regular expression to filter the exposed files. Eg: 'po/.*'"))

    allows_submission = models.BooleanField(_('Allows submission'), 
        default=False,
        help_text=_('Does this module repository allow write access?'))
    submission_type = models.CharField(_('Submit to'), blank=True, 
        max_length=10)

    hidden = models.BooleanField(_('Hidden'), default=False, editable=False,
        help_text=_('Hide this object from the list view?'))
    enabled = models.BooleanField(_('Enabled'), default=True, editable=False,
        help_text=_('Enable this object or disable its use?'))
    created = models.DateTimeField(auto_now_add=True, editable=False)
    modified = models.DateTimeField(auto_now=True, editable=False)
    should_calculate = models.BooleanField(_('Calculate statistics?'),
        default=True, help_text=_('Should statistics be calculated for '
        'this component?'))

    # Normalized fields
    full_name = models.CharField(max_length=100, editable=False)
    long_description_html = models.TextField(_('HTML Description'), 
        blank=True,
        max_length=1000, help_text=_('Description in HTML.'), editable=False)

    # Relations
    project = models.ForeignKey(Project, verbose_name=_('Project'))
    _unit = models.OneToOneField(Unit, verbose_name=_('Unit'),
        blank=True, null=True, editable=False, db_column='unit_id')
    pofiles = generic.GenericRelation(POFile)

    # Managers
    objects = ComponentManager()

    def _get_unit(self):
        if type(self._unit) == Unit:
            self._unit = self._unit.promote()
        return self._unit
    
    def _set_unit(self, newunit):
        self._unit = newunit
        
    unit = property(_get_unit, _set_unit)

    def __unicode__(self):
        return u'%s (%s)' % (self.name, self.project)

    def __repr__(self):
        return _('<Component: %s>') % self.full_name

    class Meta:
        unique_together = ("project", "slug")
        verbose_name = _('component')
        verbose_name_plural = _('components')
        db_table  = 'projects_component'
        ordering  = ('name',)
        get_latest_by = 'created'
        permissions = (
            ("clear_cache", "Can clear cache"),
            ("refresh_stats", "Can refresh statistics"),
            ("submit_file", "Can submit file"),
        )

    @cached_property
    def trans(self):
        """
        Cache TransHandler property field.

        Allow the TransHandler initialization only when it is needed.
        """
        if self.id and self.i18n_type:
            handler_class = get_trans_handler(self.i18n_type)
            return handler_class(self)

    @permalink
    def get_absolute_url(self):
        return ('component_detail', None,
                { 'project_slug': self.project.slug,
                 'component_slug': self.slug })

    def get_stats(self):
        """Get translation stats for a component listed by language."""
        return POFile.objects.by_object_total(self)

    def get_full_name(self):
        return "%s.%s" % (self.project.slug, self.slug)

    def save(self, *args, **kwargs):
        desc_escaped = escape(self.long_description)
        self.long_description_html = markdown.markdown(desc_escaped)
        self.full_name = self.get_full_name()

        if self.id:
            component_old = Component.objects.get(id=self.id)
        else:
            component_old = None

        super(Component, self).save(*args, **kwargs)

        if self.unit:
            self.unit.name = self.full_name
            self.unit.save()

        if component_old and component_old.full_name != self.full_name:
            component_old.rename_static_dir(self.full_name)

    def delete(self, *args, **kwargs):
        self.clear_cache()
        if self.unit:
            self.unit.delete()
        super(Component, self).delete(*args, **kwargs)

    def set_unit(self, root, type, branch=None, web_frontend=None):
        """
        Associate a unit with this component.

        Another place the same functionality happens is when the Component
        form is saved.
        """
        
        #TODO: Find a clever solution (less tied) for the next if
        # Necessary to recreate it when unit changes from vcs to tar 
        # and vice-versa
        if self.unit and ((self.unit.type != 'tar' and type == 'tar') or
            (self.unit.type == 'tar' and type != 'tar')):
                logger.debug("Unit type changed. Cleaning cache it for %s." % 
                    self.full_name)
                self.clear_cache()
                self.unit.delete()
                self.unit = None

        if self.unit:
            logger.debug("Updating Unit for %s." % self.full_name)
            self.unit.name = self.full_name
            # Clean the Unit repo case the root url changed
            if self.unit.root != root:
                self.clear_cache()
            self.unit.root = root
            self.unit.branch = branch
            self.unit.type = type
            self.unit.web_frontend = web_frontend
        else:
            logger.debug("Unit for %s not found. Creating." % self.full_name)
            try:
                if branch and type!='tar':
                    u = VcsUnit.objects.create(name=self.full_name, root=root,
                        type=type, branch=branch, web_frontend=web_frontend)
                else:
                    u = Tarball.objects.create(name=self.full_name, root=root,
                        type=type)
                u.save()
                self.unit = u
            except IntegrityError, e:
                logger.error("Yow! Unit exists but is not associated with %s! "
                          % self.full_name)
                print e
                # TODO: Here we should probably send an e-mail to the
                # admin, because something very strange would be happening
                pass
        return self.save()

    def get_files(self):
        """Return a list of filtered files for the component."""
        return [f for f in self.unit.get_files(self.file_filter)]

    def prepare(self):
        """
        Abstract unit.prepare().

        This function creates/updates the Component local repository
        and then unset the TransHandler property cache for it be created
        again, with a new set of files, next time that it will be used.
        """
        logger.debug("Updating local repo for %s" % self.full_name)
        Signal.send(signals.pre_comp_prep, sender=Component,
            instance=self)
        self.unit.prepare()
        del(self.trans)
        Signal.send(signals.post_comp_prep, sender=Component,
            instance=self)

    def clear_cache(self):
        """
        Clear the local cache of the component.

        Delete statistics, teardown repo, remove static dir, rest unit.
        """
        logger.debug("Clearing local cache for %s" % self.full_name)
        Signal.send(signals.pre_clear_cache, sender=Component, component=self)
        try:
            
            self.trans.clean_stats()
            self.delete_static_dir()
            self.unit.teardown()
            del(self.trans)
            if self.unit:
                self.delete_static_dir()
                self.unit.last_checkout = None
                self.unit.save()
        except:
            logger.error("Clearing cache failed for %s." % (self.full_name))
        Signal.send(signals.post_clear_cache, sender=Component, component=self)

    def get_rev(self, path=None):
        """Get revision of a path from the underlying Unit"""
        return self.unit.get_rev(path)

    def submit(self, files, msg, user):
        return self.unit.submit(files, msg, user)

    # TODO: We might want to move the next two functions to another
    # app later, like Utils or something
    def rename_static_dir(self, new_name):
        """Rename the directory of static content for a component"""
        import shutil
        try:
            original = os.path.join(settings.MSGMERGE_DIR, self.full_name)
            destination = os.path.join(settings.MSGMERGE_DIR, new_name)
            shutil.move(original, destination)
        except IOError:
            pass

    def delete_static_dir(self):
        """Delete the directory of static content for a component"""
        import shutil
        try:
            shutil.rmtree(os.path.join(settings.MSGMERGE_DIR,
                                       self.full_name))
        except OSError:
            pass

log_model(Component)


class Release(models.Model):

    """
    A release of a project, as in 'a set of specific components'.
    
    Represents the packaging and releasing of a software project (big or
    small) on a particular date, for which makes sense to track
    translations across the whole release.
    
    Examples of Releases is Transifex 1.0, GNOME 2.26, Fedora 10 etc.
    """

    slug = models.SlugField(_('Slug'), max_length=30,
        help_text=_('A short label to be used in the URL, containing only '
                    'letters, numbers, underscores or hyphens.'))
    name = models.CharField(_('Name'), max_length=50,
        help_text=_('A string like a name or very short description.'))
    description = models.CharField(_('Description'),
        blank=True, max_length=255,
        help_text=_('A sentence or two describing the object.'))
    long_description = models.TextField(_('Long description'),
        blank=True, max_length=1000,
        help_text=_('Use Markdown syntax.'))
    homepage = models.URLField(blank=True, verify_exists=False)

    release_date = models.DateTimeField(_('Release date'),
        blank=True, null=True,
        help_text=_('When this release will be available.'))
    stringfreeze_date = models.DateTimeField(_('String freeze date'),
        blank=True, null=True,
        help_text=_("When the translatable strings will be frozen (no strings "
                    "can be added/modified which affect translations."))
    develfreeze_date = models.DateTimeField(_('Devel freeze date'),
        blank=True, null=True,
        help_text=_("The last date packages from this release can be built "
                    "from the developers. Translations sent after this date "
                    "will not be included in the released version."))
    
    created = models.DateTimeField(auto_now_add=True, editable=False)
    modified = models.DateTimeField(auto_now=True, editable=False)
    
    # Normalized fields
    long_description_html = models.TextField(_('HTML Description'),
        blank=True, max_length=1000,
         help_text=_('Description in HTML.'), editable=False)

    # Relations
    project = models.ForeignKey(Project, verbose_name=_('Project'), related_name='releases')
    components = models.ManyToManyField(Component,
        verbose_name=_('Components'), related_name='releases',
        blank=True, null=True)

    def __unicode__(self):
        return self.name

    def __repr__(self):
        return _('<Release: %(rel)s (Project %(proj)s)>') % {
            'rel': self.name,
            'proj': self.project.name}
    
    @property
    def full_name(self):
        return "%s (%s)" % (self.name, self.project.name)

    @property
    def pofiles(self):
        return POFile.objects.by_release_total(self)

    @property
    def pofiles_for_language(self, language):
        return POFile.objects.by_release_and_language_total(self, language)

    class Meta:
        unique_together = ("slug", "project")
        verbose_name = _('release')
        verbose_name_plural = _('releases')
        ordering  = ('name',)
        get_latest_by = 'created'

    def save(self, *args, **kwargs):
        import markdown
        from cgi import escape
        desc_escaped = escape(self.long_description)
        self.long_description_html = markdown.markdown(desc_escaped)
        created = self.created
        super(Release, self).save(*args, **kwargs)

    @permalink
    def get_absolute_url(self):
        return ('release_detail', None,
                { 'project_slug': self.project.slug,
                 'release_slug': self.slug })

log_model(Release)
