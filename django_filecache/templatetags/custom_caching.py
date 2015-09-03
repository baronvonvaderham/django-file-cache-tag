from django import template
from adv_cache_tag.tag import CacheTag
import hashlib
from django.utils.http import urlquote
from django.core.cache import cache

# Extending the CacheTag class from django-adv-cache-tag
class FileBasedCacheTag(CacheTag):

    # Sets back-end for this tag to be something else in CACHES[] besides 'default'
    class Meta(CacheTag.Meta):
        cache_backend = 'filecache'
        takes_context = 'true'

    # Method overriding default assignment of key
    def get_base_cache_key(self):
        args = self.get_cache_key_args()
        path = template.resolve_variable(args['name'], self.context)
        key = 'filecache.' + path + '.' +args['hash']
        return key

# Register the tag for use
register = template.Library()
FileBasedCacheTag.register(register, 'file_cache')

# Tag to allow creation of new variables in template
@register.assignment_tag
def define(the_string):
    return the_string

# Hashes the list of parameters and constructs the file-based cache key
def generate_cache_key(url, vary_on):
    hash = hashlib.md5(u':'.join([urlquote(var) for var in vary_on])).hexdigest()
    key = 'file_cache.' + url + '.' + hash
    return key

# Manually invalidates cache for key provided
def invalidate_filecache(key):
    file_cache = cache.get_cache('filecache')
    file_cache.delete(key)
