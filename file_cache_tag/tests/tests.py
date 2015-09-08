from django.test import TestCase
from django.test.client import Client
import django.core.cache as cache
from file_cache_tag.templatetags import custom_caching
from shutil import rmtree

from django.conf import global_settings


class DemoSiteTest(TestCase):
    def setUp(self):
        self.client = Client()

    def tearDown(self):
        rmtree(global_settings.FILECACHE_DIRECTORY)

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
