#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
#  This file is part of django-context-extras.
#
#  django-context-extras provides some extra context processors for Django
#  projects.
#
#  Development Web Site:
#    - http://www.codetrax.org/projects/django-context-extras
#
#  Sponsored by:
#    - http://www.g-loaded.eu/
#    - http://www.codetrax.org/
#
#  Copyright (c) 2010 George Notaras <gnot@g-loaded.eu>
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
sys.path.append(os.path.abspath('src'))

from setuptools import setup, find_packages

from context_extras import get_version 


if __name__=='__main__':
    setup(
        name = 'django-context-extras',
        version = get_version(),
        author = 'George Notaras',
        author_email = 'gnot@g-loaded.eu',
        maintainer = 'George Notaras',
        maintainer_email = 'gnot@g-loaded.eu',
        url = 'http://www.codetrax.org/projects/django-context-extras',
        description = 'django-context-extras provides some extra context processors for Django projects.',
        long_description = 'django-context-extras provides some extra context processors for Django projects.',
        download_url = 'https://source.codetrax.org/hgroot/django-context-extras',
        classifiers = [
            'Development Status :: 4 - Beta',
            'Environment :: Web Environment',
            'Framework :: Django',
            'Intended Audience :: Developers',
            'License :: OSI Approved :: Apache Software License',
            'Natural Language :: English',
            'Operating System :: OS Independent',
            'Programming Language :: Python',
            'Topic :: Software Development :: Libraries :: Application Frameworks',
            'Topic :: Software Development :: Libraries :: Python Modules',
        ],
        license = 'Apache License version 2',
        package_dir = {'': 'src'},
        packages = find_packages(),
        include_package_data = True,
    )

