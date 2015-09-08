import os
import sys
import django

BASE_PATH = os.path.dirname(__file__)


def main():
    """
    Standalone django model test with a 'memory-only-django-installation'.
    You can play with a django model without a complete django app installation
    http://www.djangosnippets.org/snippets/1044/
    """
    sys.exc_clear()

    os.environ["DJANGO_SETTINGS_MODULE"] = "django.conf.global_settings"
    from django.conf import global_settings

    global_settings.INSTALLED_APPS = (
        'adv_cache_tag',
        'file_cache_tag',
    )
    global_settings.CELERY_ALWAYS_EAGER = True

    if django.VERSION > (1, 2):
        global_settings.DATABASES = {
            'default': {
                'ENGINE': 'django.db.backends.sqlite3',
                'NAME': os.path.join(BASE_PATH, 'connpass.sqlite'),
                'USER': '',
                'PASSWORD': '',
                'HOST': '',
                'PORT': '',
            }
        }
    else:
        global_settings.DATABASE_ENGINE = "sqlite3"
        global_settings.DATABASE_NAME = ":memory:"

    global_settings.ROOT_URLCONF = 'file_cache_tag.tests.demo_app.urls'

    global_settings.TEMPLATE_DIRS = (os.path.join(BASE_PATH, 'file_cache_tag/tests/demo_app/templates'),)

    global_settings.TEMPLATE_CONTEXT_PROCESSORS = (
            'django.core.context_processors.static',
            'django.core.context_processors.media',
            'django.contrib.messages.context_processors.messages',
            "django.contrib.auth.context_processors.auth",
            'django.core.context_processors.request',
            )

    global_settings.FILECACHE_DIRECTORY = os.environ.get("FILECACHE_DIRECTORY", os.path.join(BASE_PATH, 'CACHE/filecache/'))

    global_settings.CACHES = {
        'default': {
            'BACKEND': 'django.core.cache.backends.dummy.DummyCache'
        },
        'filecache': {
            'BACKEND': 'django.core.cache.backends.filebased.FileBasedCache',
            'LOCATION': global_settings.FILECACHE_DIRECTORY,
    }
}

    global_settings.MIDDLEWARE_CLASSES = (
        'django.middleware.cache.UpdateCacheMiddleware',
        'django.middleware.common.CommonMiddleware',
        'django.contrib.sessions.middleware.SessionMiddleware',
        'django.contrib.auth.middleware.AuthenticationMiddleware',
        'django.middleware.cache.FetchFromCacheMiddleware',
        'django.contrib.messages.middleware.MessageMiddleware',
    )

    global_settings.SECRET_KEY = "blahblah"
    global_settings.DEBUG = True
    global_settings.TEMPLATE_DUBUG = True

    from django.test.utils import get_runner
    test_runner = get_runner(global_settings)

    if django.VERSION > (1, 7):
        django.setup()

    if django.VERSION > (1, 2):
        test_runner = test_runner()
        failures = test_runner.run_tests(['file_cache_tag'])
    else:
        failures = test_runner(['file_cache_tag'], verbosity=2)
    sys.exit(failures)

if __name__ == '__main__':
    main()
