================
django_filecache
================

This package provides a custom template tag library that allows
the user to implement a secondary cache back-end without altering
their default in CACHES[].

This is currently configured for a file-based cache that parses
the URL of the requested page and a list of vary_on attributes
to generate unique cache keys. It can be easily modified to
accommodate other methods of key generation and other cache
back-ends, or extended to create additional tags for yet more
caches side by side.

Installation
------------

1.  Add "-e git+https://github.com/baronvonvaderham/django-filecache.git#egg=filecache"
    to requirements.txt in your project (not on pypi yet).

2.  Add "filecache" to your INSTALLED_APPS setting like this::

        INSTALLED_APPS = (
            ...
            'django_filecache',
        )

3.  Run "pip install -r requirements.txt" from your project's
    directory to install required packages.

4. Run "python manage.py migrate" to create the required models.

5. Modify your CACHES setting like this::

    CACHES = {
        'default': {
            ...
        },
        'filecache': {
            'BACKEND': 'django.core.cache.backends.filebased.FileBasedCache',
            'LOCATION': FILECACHE_DIRECTORY,
        }
    }

6. Add a FILECACHE_DIRECTORY setting to settings.py, either as an absolute path or as accepting an environment variable::

    FILECACHE_DIRECTORY = os.environ.get("FILECACHE_DIRECTORY", "/CACHE/filecache/")

Example Usage
-------------

Templates::

        {% file_cache [expiration time] request.get_full_path arg1 arg2 ... %}

    Any number of args can be accepted into the tag. All will be hashed and
    returned in FileBasedCacheTag.get_cache_key_args()['hash'].

Views:

    Methods from this package will be called within views to manually reconstruct
    cache keys and invalidate individual cache versions. A separate method is provided
    for key generation and invalidation. It is important to provide the arguments used
    in the template for that view in the same order in a simple list, and to loop
    through all possible keys within the view itself; the package will not know to
    find each possible version of the page.

    This is most often implemented at the end of a method that updates a model being
    displayed. This ensures that as of the time of saving new data, the cache is now
    invalid.
