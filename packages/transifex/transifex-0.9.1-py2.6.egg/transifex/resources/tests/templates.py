# -*- coding: utf-8 -*-
from django.conf import settings
from django.core.urlresolvers import reverse
from txcommon.tests.base import BaseTestCase
from resources.models import SourceEntity


class ResourcesTemplateTests(BaseTestCase):

    def setUp(self):
        super(ResourcesTemplateTests, self).setUp()
        #URL
        self.resource_detail_url = reverse('resource_detail',
            args=[self.project.slug, self.resource.slug])
        self.project_detail_url = reverse('project_detail', 
            args=[self.project.slug]) 

    def tearDown(self):
        super(ResourcesTemplateTests, self).tearDown()

    def test_create_resource_template_tag(self):
        """Ensure that button and the form is appeared correctly."""
        resp = self.client['maintainer'].get(self.project_detail_url)
        self.assertTemplateUsed(resp,
                                'projects/resource_list.html')
        self.assertContains(resp,
                            "Create Resource")
        for user in ['anonymous', 'registered','team_member']:
            resp = self.client[user].get(self.project_detail_url)
            self.assertNotContains(resp,
                                   "Create Resource")

    def test_priority_table_snippet(self):
        """ Check that priority td is presented correctly."""
        resp = self.client['maintainer'].get(self.project_detail_url)
        self.assertTemplateUsed(resp, 'projects/resource_list.html')
        self.assertContains(resp,
                            'id="priority_%s"' % 
                            (self.resource.slug ,),
                            status_code=200)
        self.assertContains(resp,
                            '<span class="priority_sort" style="display:none">%s</span>' %
                            (self.resource.priority.level ,))
        self.assertContains(resp,
                            '<img src="%spriorities/images/%s.png"' %
                            (settings.STATIC_URL, 
                             self.resource.priority.display_level ))
        for user in ['anonymous', 'registered','team_member']:
            resp = self.client[user].get(self.project_detail_url)
            self.assertNotContains(resp,
                                   'id="priority_%s"' % 
                                   (self.resource.slug ,),
                                   status_code=200)

    def test_edit_delete_buttons_per_resource(self):
        """ Test that edit/delete buttons appear only for maintainer in 
        resource_list.html"""
        resp = self.client['maintainer'].get(self.project_detail_url)
        self.assertTemplateUsed(resp, 'projects/resource_list.html')
        self.assertContains(resp,
                            '<a href="%s">edit</a>' % 
                            (reverse('resource_edit', 
                                     args=[self.project.slug,
                                           self.resource.slug]),),
                            status_code=200)
        self.assertContains(resp,
                            '<a href="%s">del</a>' %
                            (reverse('resource_delete', 
                                     args=[self.project.slug,
                                           self.resource.slug])),
                            status_code=200)
        # All the other user classes should not see these snippets
        for user in ['anonymous', 'registered','team_member']:
            resp = self.client[user].get(self.project_detail_url)
            self.assertNotContains(resp,
                                '<a href="%s">edit</a>' % 
                                (reverse('resource_edit', 
                                         args=[self.project.slug,
                                               self.resource.slug]),),
                                status_code=200)
            self.assertNotContains(resp,
                                '<a href="%s">del</a>' %
                                (reverse('resource_delete', 
                                         args=[self.project.slug,
                                               self.resource.slug])),
                                status_code=200)

    def test_available_langs_per_resource(self):
        """ Test that the correct number of resource languages appear in template."""
        self.assertEqual(type(self.resource.available_languages.count()), int)
        for user in ['anonymous', 'registered','team_member', 'maintainer']:
            resp = self.client[user].get(self.project_detail_url)
            self.assertContains(resp, 'Available Languages: %s' %
                                (self.resource.available_languages.count()))

    def test_total_strings_per_resource(self):
        """Test that resource.total_entities return the correct amount of
        strings in the resource_list page."""
        self.assertEqual(self.resource.entities_count, 
                         SourceEntity.objects.filter(
                             resource=self.resource).count())
        for user in ['anonymous', 'registered','team_member', 'maintainer']:
            resp = self.client[user].get(self.project_detail_url)
            self.assertContains(resp, 'title="Total Strings: %s' %
                                (self.resource.entities_count))

    def test_javascript_snippet_cycle_priority(self):
        """Test if we include the ajax triggering js for priority changes."""
        resp = self.client['maintainer'].get(self.project_detail_url)
        self.assertTemplateUsed(resp, 'projects/resource_list.html')
        self.assertContains(resp,
                            'var resource_priority_cycle_url = \'%s\';'% 
                            (reverse('cycle_resource_priority', 
                                     args=[self.project.slug, "1111111111"]),),
                            status_code=200)
        self.assertContains(resp,
                            'title="Click the flags to modify the importance of a resource."')
        # All the other user classes should not see these snippets
        for user in ['anonymous', 'registered','team_member']:
            resp = self.client[user].get(self.project_detail_url)
            self.assertNotContains(resp,
                                'var resource_priority_cycle_url = \'%s\';'% 
                                (reverse('cycle_resource_priority', 
                                         args=[self.project.slug, "1111111111"]),),
                                status_code=200)
            self.assertNotContains(resp,
                                'title="Click the flags to modify the importance of a resource."')

    def test_translate_resource_button(self):
        """Test that translate resource button appears in resource details."""
        # Test the response contents
        for user in ['team_member', 'maintainer']:
            resp = self.client[user].get(self.resource_detail_url)
            self.assertTemplateUsed(resp, 'resources/resource.html')
            self.assertContains(resp,
                                '<a id="new_translation1" class="buttonized i16 add">Translate Resource</a>',
                                status_code=200)
        # The anonymous users and the non-team members must not see the button
        for user in ['anonymous', 'registered']:
            resp = self.client[user].get(self.resource_detail_url)
            self.assertNotContains(resp,
                                '<a id="new_translation1" class="buttonized i16 add">Translate Resource</a>',
                                status_code=200)

    def test_resource_edit_button(self):
        """Test that resource edit button is rendered correctly in details."""
        # Test the response contents
        resp = self.client['maintainer'].get(self.resource_detail_url)
        self.assertTemplateUsed(resp, 'resources/resource.html')
        self.assertContains(resp,
                            '<a class="i16 edit buttonized" href="/projects/p/%s/resource/%s/edit">Edit</a>' % 
                            (self.project.slug, self.resource.slug),
                            status_code=200)
        # In any other case of user this should not be rendered
        for user in ['anonymous', 'registered', 'team_member']:
            resp = self.client[user].get(self.resource_detail_url)
            self.assertNotContains(resp,
                                '<a class="i16 edit buttonized" href="/projects/p/%s/resource/%s/edit">Edit</a>' %
                                (self.project.slug, self.resource.slug),
                                status_code=200)

    def test_delete_translation_resource_button(self):
        """Test that delete translation resource button is rendered correctly."""
        resp = self.client['maintainer'].get(self.resource_detail_url)
        self.assertTemplateUsed(resp, 'resources/resource.html')
        self.assertContains(resp,
                            '<a class="i16 edit buttonized" href="/projects/p/%s/resource/%s/edit">Edit</a>' % 
                            (self.project.slug, self.resource.slug),
                            status_code=200)
        # In any other case of user this should not be rendered
        for user in ['anonymous', 'registered', 'team_member']:
            resp = self.client[user].get(self.resource_detail_url)
            self.assertNotContains(resp,
                                '<a class="i16 delete buttonized" href="/projects/p/%s/resource/%s/delete">Delete translation resource</a>' %
                                (self.project.slug, self.resource.slug),
                                status_code=200)