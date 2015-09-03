#!/usr/bin/env python
from setuptools import setup, find_packages
import os


# Utility function to read README file
def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name='django-file-cache-tag',
    version='0.1',
    description="Provides an custom template tag library for template fragment caching with a non-default back-end.",
    author="Scott Johnson",
    author_email='ben@aashe.org',
    url='https://github.com/aashe/django-file-cache-tag',
    long_description=read("README.rst"),
    packages=[
        'file_cache_tag',
        ],
    classifiers=[
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2.7',
        'Framework :: Django',
    ],
    test_suite='tests.main',
    install_requires=['Django', 'django-adv-cache-tag'],
)
