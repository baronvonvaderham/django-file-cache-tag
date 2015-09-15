from django.test import TestCase
from django.test.client import Client
from django.contrib.auth.models import User
import django.core.cache as cache
from file_cache_tag.templatetags import custom_caching
from shutil import rmtree

from django.conf import global_settings
import os


class DemoSiteTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.staff_client = Client()

    def tearDown(self):
        pass

    # Test that the demo_app generic view works
    def test_base_view(self):
        response = self.client.get('/test/')
        self.assertEqual(response.status_code, 200)

    # Test to see if a cache was generated with the correct key for the page
    def test_create_cache(self):
        response = self.client.get('/test/')
        key = custom_caching.generate_cache_key('/test/', ['anon'])
        filecache = cache.get_cache('filecache')
        cached = filecache.get(key)
        self.assertTrue(cached)

    # Test to see if invalidation function deletes the cached page correctly
    def test_invalidate_cache(self):
        response = self.client.get('/test/')
        key = custom_caching.generate_cache_key('/test/', ['anon'])
        filecache = cache.get_cache('filecache')
        cached = filecache.get(key)
        custom_caching.invalidate_filecache(key)
        no_more_cache = filecache.get(key)
        self.assertTrue(cached)
        self.assertFalse(no_more_cache)

    def test_versioning(self):
        username = 'scott'
        password = 'top_secret'
        email = 'fake@email.com'
        self.staff_user = User.objects.create_superuser(
            username=username, email=email, password=password)
        is_authenticated = self.staff_client.login(username=username, password=password)
        self.assertTrue(is_authenticated)

        filecache = cache.get_cache('filecache')

        # Make initial requests to create caches
        anon_response = self.client.get('/test/')
        staff_response = self.staff_client.get('/test/')
        self.assertNotEqual(anon_response, staff_response)

        # Verify caches were created
        anon_key = custom_caching.generate_cache_key('/test/', ['anon'])
        staff_key = custom_caching.generate_cache_key('/test/', ['staff'])
        anon_cached = filecache.get(anon_key)
        staff_cached = filecache.get(staff_key)
        self.assertTrue(anon_cached)
        self.assertTrue(staff_cached)

        # Verify they are not identical versions
        self.assertNotEqual(anon_cached, staff_cached)

        # Verify that the served cached versions on subsequent requests also vary
        anon_cached_response = self.client.get('/test/')
        staff_cached_response = self.staff_client.get('/test/')
        self.assertNotEqual(anon_cached_response, staff_cached_response)

        # Finally, verify both caches can be invalidated
        custom_caching.invalidate_filecache(anon_key)
        custom_caching.invalidate_filecache(staff_key)
        no_more_anon_cache = filecache.get(anon_key)
        no_more_staff_cache = filecache.get(staff_key)
        self.assertFalse(no_more_anon_cache)
        self.assertFalse(no_more_staff_cache)
