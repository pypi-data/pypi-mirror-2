# -*- coding: utf-8 -*-
try:
    import json
except ImportError:
    import simplejson as json

from django.core.urlresolvers import reverse
from django.db.models import get_model
from django.test.client import Client
from resources.models import Resource, Translation, SourceEntity
from resources.tests.api.base import APIBaseTests
from resources.tests.api.utils import create_auth_string
from txcommon.tests.base import PASSWORD

class StringHandlerTests(APIBaseTests):
    """Tests for the StringHandler API."""
    def setUp(self):
        super(StringHandlerTests, self).setUp()
        self.resource = Resource.objects.create(name="test", slug="test",
            project=self.project,
            source_language=self.language_en)
        self.resource_handler_url = reverse('string_resource_push',
            args=[self.project.slug, self.resource.slug])

    def tearDown(self):
        self.resource.delete()

    def test_api_get(self):
        """ Test GET method."""


        # User info for authentication
        username = 'maintainer'
        password = PASSWORD

        auth_string = create_auth_string(username, password)
        client = Client()

        # Create resource with initial strings to test GET
        resp = client.post(self.resource_handler_url, json.dumps(self.data),
                                content_type='application/json',
                                HTTP_AUTHORIZATION=auth_string)
        self.assertEqual(resp.status_code, 201)

        response = self.client['maintainer'].get(self.resource_handler_url)
        json_data = json.loads(response.content)[0] # get 1st resource
        # Check that we got all translation strings
        self.assertEqual(len(json_data['strings']),
                            Translation.objects.filter(
                            source_entity__resource = self.resource,
                            language = self.resource.source_language).count())

        self.assertTrue(self.resource.source_language.code in response.content)
        for t in Translation.objects.filter(
                        source_entity__resource__slug = self.resource,
                        language__code = self.resource.source_language):
            self.assertTrue(t.string in response.content)
            self.assertTrue(t.source_entity.context in response.content)



    def test_api_post(self):
        """ Test POST method."""

        # User info for authentication
        password = PASSWORD
        username = 'maintainer'

        response = self.client['maintainer'].post(self.resource_handler_url,
            self.data, 'application/json')
        self.assertEquals(response.status_code, 400)

        auth_string = create_auth_string(username, password)
        client = Client()

        # Maintainer should be able to create the tresource
        resp = client.post(self.resource_handler_url,json.dumps(self.data),
                                content_type='application/json',
                                HTTP_AUTHORIZATION=auth_string)
        self.assertEqual(resp.status_code, 201)

        # Check if resource was created
        self.assertEqual(Resource.objects.filter(project = self.project,
                            slug = self.resource.slug).count(), 1)

        # Check source entities
        self.assertEqual(SourceEntity.objects.filter(
                            resource__slug = self.resource.slug).count(),
                            len(self.data['strings']))

        # Check that all strings are there
        self.assertEqual(Translation.objects.filter(
                            source_entity__resource = self.resource,
                            language = self.resource.source_language).count(),
                            len(self.data['strings']))


        # Regular user should not be able to post.
        # TODO: Fix permissions and then uncomment the following

        #username = 'registered'
        #password = PASSWORD
        #auth_string = create_auth_string(username, password)
        #resp = self.client['maintainer'].post(self.resource_project_url,json.dumps(self.data),
        #                                    content_type='application/json',
        #                                    HTTP_AUTHORIZATION=auth_string)
        #self.assertEqual(resp.status_code, 403)


    def test_api_put(self):
        """ Test PUT method."""

        # PUT has an issue fixed in django 1.1.2 (Django 1.1.1 throws error) 
        # http://code.djangoproject.com/ticket/11371

        # User info for authentication
        username = 'maintainer'
        password = PASSWORD

        response = self.client['maintainer'].post(self.resource_handler_url,
            self.data, 'application/json')
        self.assertEqual(response.status_code, 400)

        # Create auth headers
        auth_string = create_auth_string(username, password)
        client = Client()

        handler_url = reverse('string_resource_push',
            args=[self.project.slug, self.resource.slug])

        # Create the resource and source entities
        resp = client.post(self.resource_handler_url,json.dumps(self.data),
                                content_type='application/json',
                                HTTP_AUTHORIZATION=auth_string)
        self.assertEqual(resp.status_code, 201)

        self.resource_string_handler_url = reverse('string_resource_pullfrom',
            args=[self.project.slug, self.resource.slug, self.language.code])


        # Create the new translation strings
        resp = client.put(self.resource_string_handler_url,json.dumps(self.trans),
                                content_type='application/json',
                                HTTP_AUTHORIZATION=auth_string)
        self.assertEqual(resp.status_code, 200)

        # Check that all strings are in the db
        self.assertEqual(Translation.objects.filter(
                            source_entity__resource__slug = self.resource.slug,
                            language__code = self.language.code).count(),
                            len(self.trans['strings']))


    def test_api_delete(self):
        """ Test DELETE method."""
        #response = self.client['maintainer'].delete(self.resource_handler_url,
        #    self.data, 'application/json')
        pass
