#!/usr/bin/env python
#
#  Copyright (c) 2010 nl_0
#
#  This file is part of django-saddle.
#
#  django-saddle is free software distributed under terms of BSD Licence.
#  See the LICENSE file for copying conditions.
#

"django-saddle setup"

from setuptools import setup, find_packages
import saddle

setup(
    name         = 'django-saddle',
    version      = saddle.__version__,
    packages     = find_packages(exclude=['tmpl']),

    requires     = ['python (>= 2.4)', 'django (>= 1.2)'],
    provides     = ['saddle'],

    description  = 'Settings on steroids and some shortcuts for Django',
    long_description = 'django-saddle is an application aimed to simplify typical'
                       ' tasks related to creating a Django-powered website,'
                       ' maintaining several instances (local, production, etc.)'
                       ' and tracking requirements.',
    author       = 'nl_0',
    author_email = 'nl_0@mail.ru',
    url          = 'http://bitbucket.org/nl_0/django-saddle/',
    download_url = 'http://bitbucket.org/nl_0/django-saddle/downloads/',
    license      = 'BSD License',
    keywords     = 'django settings conf virtualenv pip',
    classifiers  = [
        'Development Status :: 3 - Alpha',
        'Environment :: Web Environment',
        'Environment :: Console',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
)
