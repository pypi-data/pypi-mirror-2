# encoding: utf-8
#
# Distribute metadata for sk.recipe.xdv
# 
# Copyright 2010 Sean Kelly and contributors.
# This is licensed software. Please see the LICENSE.txt file for details.

from setuptools import setup, find_packages
import os.path

_name = 'sk.recipe.xdv'
_desc = 'A recipe for Buildout (zc.buildout) to compile XDV rules into XSLT'
_version = '0.0.0'
_keywords = 'buildout xdv deliverance compiler xsl xslt'
_url, _downloadURL = 'http://code.google.com/p/buildout-recipes/', 'http://code.google.com/p/buildout-recipes/downloads/list'
_author, _authorEmail = 'Sean Kelly', 'kelly@seankelly.biz'
_license = 'BSD'
_namespaces = ['sk', 'sk.recipe']
_entryPoints = {
    'zc.buildout': [
        'default = %s:Recipe' % _name,
        'install = %s:Recipe' % _name,
    ]
}
_zipSafe = True
_testSuite = '%s.tests.test_suite' % _name
_requirements = [
    'setuptools',
    'zc.buildout >=1.2.0',
    'xdv >=0.3',
]
_testRequirements = [
    'zope.testing',
]
_classifiers = [
    'Development Status :: 2 - Pre-Alpha',
    'Environment :: Console',
    'Framework :: Buildout',
    'Intended Audience :: Developers',
    'License :: OSI Approved :: BSD License',
    'Operating System :: OS Independent',
    'Programming Language :: Python',
    'Topic :: Software Development :: Build Tools',
    'Topic :: Text Processing :: Markup :: XML',
]

def _read(*rnames):
    return open(os.path.join(os.path.dirname(__file__), *rnames)).read()

_header = '*' * len(_name) + '\n' + _name + '\n' + '*' * len(_name)
_longDesc = '\n\n'.join([
    _header,
    _read('README.txt'),
    _read('docs', 'INSTALL.txt'),
    _read('sk', 'recipe', 'xdv', 'README.txt'),
    _read('docs', 'HISTORY.txt'),
])
open('doc.txt', 'w').write(_longDesc)

setup(
    author=_author,
    author_email=_authorEmail,
    classifiers=_classifiers,
    description=_desc,
    download_url=_downloadURL,
    entry_points=_entryPoints,
    include_package_data=True,
    install_requires=_requirements,
    keywords=_keywords,
    license=_license,
    long_description=_longDesc,
    name=_name,
    namespace_packages=_namespaces,
    packages=find_packages(exclude=['ez_setup']),
    tests_require=_testRequirements,
    test_suite=_testSuite,
    url=_url,
    version=_version,
    zip_safe=_zipSafe,
)
