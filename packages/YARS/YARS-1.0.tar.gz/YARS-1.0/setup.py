#!/usr/bin/env python
#
# Copyright 2010 W-Mark Kubacki (the "Author")
#
# Licensed under the RECIPROCAL PUBLIC LICENSE, Version 1.1 or later
# (the "License"); you may not use this file except in compliance
# with the License. You may obtain a copy of the License at
#
#     http://www.opensource.org/licenses/rpl.php
#
# In addition to the License you agree on notifying the Author by email
# about changes you publish within two weeks. You notification has to
# contain a link to the publication or you must sent the Author a copy
# of the publication. You have to add the changes (either as patch or
# a new distribution, whatever you published) as attachment to that
# notification email.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

import distutils.core
import sys
# Importing setuptools adds some features like "setup.py develop", but
# it's optional so swallow the error if it's not there.
try:
    import setuptools
except ImportError:
    pass

import yars

major, minor = sys.version_info[:2]
python_27_or_later = major > 2 or (major == 2 and minor >= 7)

requirements = [
    "redis >= 2.0.0",
    "configobj",
    "feedparser",
]
if not python_27_or_later:
    requirements.append("argparse")

distutils.core.setup(
    name="YARS",
    version=yars.__version__,
    py_modules = ["yars",],
    scripts = ["yars",],
    author="W-Mark Kubacki",
    author_email="wmark+yars@hurrikane.de",
    url="http://mark.ossdl.de/tags/yars",
    download_url="http://mark.ossdl.de/tags/yars",
    license="http://www.opensource.org/licenses/rpl.php",
    keywords=['RSS', 'feeds', 'atom', 'cdf'],
    description="Yet Another RSS downloader",
    long_description=open('README.txt','r').read(),
    install_requires=requirements,
    platforms=['POSIX', 'Windows'],
    classifiers = [
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Intended Audience :: End Users/Desktop',
        'Intended Audience :: System Administrators',
        'License :: Free for non-commercial use',
        'License :: Other/Proprietary License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Communications',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Other/Nonlisted Topic',
        'Topic :: Communications :: File Sharing',
        'Topic :: Software Development :: Libraries :: Python Modules',
        ],
)
