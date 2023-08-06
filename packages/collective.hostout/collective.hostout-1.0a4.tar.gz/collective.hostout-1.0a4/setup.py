##############################################################################
#
# Copyright (c) 2006 Zope Corporation and Contributors.
# All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#
##############################################################################

import os
from setuptools import setup, find_packages

def read(*rnames):
    return open(os.path.join(os.path.dirname(__file__), *rnames)).read()

name = "collective.hostout"
setup(
    name = name,
    version = "1.0a4",
    author = "Dylan Jay",
    author_email = "software@pretaweb.com",
    description = """collective.hostout will help you control multiple application environments
    with the minimum amount of effort. You can manage local, staging and deployment environments
    with one easy tool.""",
    license = "GPL",
    keywords = "buildout, fabric, deploy, deployment, server, plone, django, host, hosting",
    classifiers = [
        'Framework :: Buildout',
        "Development Status :: 3 - Alpha",
        "Topic :: Utilities",],
    url='https://svn.plone.org/svn/collective/'+name,
    long_description=(
        read('README.rst')
        + '\n' +
        read('CHANGES.txt')
        + '\n' 
        ),

    packages = find_packages(),
    include_package_data = True,
#    data_files = [('.', ['*.txt'])],
#    package_data = {'':('*.txt')},
    namespace_packages = ['collective'],
    install_requires = ['zc.buildout',
                        'zc.recipe.egg',
                        'setuptools',
                        'Fabric',
                        'paramiko'
                        ],
    entry_points = {'zc.buildout': ['default = collective.hostout:Recipe',],
                    'console_scripts': ['hostout = collective.hostout.hostout:main'],
                    'fabric': ['fabfile = collective.hostout.fabfile']
                    },
    zip_safe = False,
    )
