#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
#  This file is part of django-postgresql-manager.
#
#  django-postgresql-manager - a Django application which can be used to manage
#  PostgreSQL users and databases.
#
#  Development Web Site:
#    - http://www.codetrax.org/projects/django-postgresql-manager
#  Public Source Code Repository:
#    - https://source.codetrax.org/hgroot/django-postgresql-manager
#
#  Copyright 2010 George Notaras <gnot [at] g-loaded.eu>
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.
#
#  NOTES
#
#  Create source distribution tarball:
#    python setup.py sdist --formats=gztar
#
#  Create binary distribution rpm:
#    python setup.py bdist --formats=rpm
#
#  Create binary distribution rpm with being able to change an option:
#    python setup.py bdist_rpm --release 7
#
#  Test installation:
#    python setup.py install --prefix=/usr --root=/tmp
#
#  Install:
#    python setup.py install
#  Or:
#    python setup.py install --prefix=/usr
#

import sys
import os
sys.path.insert(0, os.path.abspath('src'))

from setuptools import setup

from PostgreSQL_manager import get_version, long_description

if __name__=='__main__':
    setup(
        name = 'django-postgresql-manager',
        version = get_version(),
        license = 'Apache License version 2',
        author = 'George Notaras',
        author_email = 'gnot [at] g-loaded.eu',
        maintainer = 'George Notaras',
        maintainer_email = 'gnot [at] g-loaded.eu',
        url = 'http://www.codetrax.org/projects/django-postgresql-manager',
        description = 'A Django application which can be used to manage PostgreSQL users and databases.',
        long_description = long_description,
        download_url = 'https://source.codetrax.org/hgroot/django-postgresql-manager',
        classifiers = [
            'Development Status :: 4 - Beta',
            'Environment :: Web Environment',
            'Framework :: Django',
            'Intended Audience :: Developers',
            'License :: OSI Approved :: Apache Software License',
            'Natural Language :: English',
            'Operating System :: OS Independent',
            'Programming Language :: Python',
            'Topic :: Database :: Front-Ends',
            'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
            'Topic :: Software Development :: Libraries :: Application Frameworks',
            'Topic :: Software Development :: Libraries :: Python Modules',
        ],
        package_dir = {'': 'src'},
        packages = ['PostgreSQL_manager'],
        include_package_data = True,
        #zip_safe = False,
    )

