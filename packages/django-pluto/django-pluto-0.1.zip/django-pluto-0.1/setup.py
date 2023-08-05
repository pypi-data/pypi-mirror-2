#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

setup(
    name = "django-pluto",
    description = """Pluto aims to provide an architecture to manually import 
                     articles from other feeds and provide them as a new feed 
                     or for integration into other parts of a Django project.""",
    license = 'MIT',
    version = "0.1",
    author = 'Michael Gruenewald, ActiveState Software Inc.',
    url = 'http://bitbucket.org/activestate/django-pluto/',
    download_url = 'http://bitbucket.org/activestate/django-pluto/downloads/',
    packages = find_packages(),
    classifiers = [
        'Development Status :: 4 - Beta',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP',
    ]
)
