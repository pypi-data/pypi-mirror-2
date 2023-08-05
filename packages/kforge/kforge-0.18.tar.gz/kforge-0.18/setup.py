#!/usr/bin/env python
import os
import sys

from setuptools import setup, find_packages

sys.path.insert(0, './src')
from kforge import __version__

basePath = os.path.abspath(os.path.dirname(sys.argv[0]))
scripts = [ 
    os.path.join('bin', 'kforge-makeconfig'),
    os.path.join('bin', 'kforge-admin'),
    os.path.join('bin', 'kforge-test'),
]

setup(
    name='kforge',
    version=__version__,

    package_dir={'': 'src'},
    packages=find_packages('src'),
    scripts=scripts,
    # just use auto-include and specify special items in MANIFEST.in
    include_package_data = True,
    # ensure KForge is installed unzipped
    # this avoids potential problems when apache/modpython imports kforge but
    # does not have right permissions to create an egg-cache directory
    # see:
    # http://mail.python.org/pipermail/python-list/2006-September/402300.html
    # http://docs.turbogears.org/1.0/mod_python#setting-the-egg-cache-directory
    zip_safe = False,

    install_requires = [
        'domainmodel==0.8',
        'Routes>=1.7.2,<=1.10.3',
        'rawdog',
    ],
    # format section name (plugin type), module.path:Class [requirements]
    entry_points = '''
    [kforge.plugins]
    # --------------
    # System Plugins
    accesscontrol = kforge.plugin.accesscontrol:Plugin
    apacheconfig = kforge.plugin.apacheconfig:Plugin
    notify = kforge.plugin.notify:Plugin
    # --------------
    # Service Plugins 
    dav = kforge.plugin.dav:Plugin
    joomla = kforge.plugin.joomla:Plugin
    mailman = kforge.plugin.mailman:Plugin
    moin = kforge.plugin.moin:Plugin 
    svn = kforge.plugin.svn:Plugin
    # leave dependency out for time being
    # trac = kforge.plugin.trac:Plugin [trac]
    trac = kforge.plugin.trac:Plugin
    wordpress = kforge.plugin.wordpress:Plugin
    www = kforge.plugin.www:Plugin
    mercurial = kforge.plugin.mercurial:Plugin
    # --------------
    # Testing Plugins
    example = kforge.plugin.example:Plugin
    example_non_service = kforge.plugin.example_non_service:Plugin
    example_single_service = kforge.plugin.example_single_service:Plugin
    testingexample = kforge.plugin.testingexample:Plugin
    ''',
    extras_require = { 'trac' : 'trac >= 0.8' },

    author='Open Knowledge Foundation and Appropriate Software Foundation',
    author_email='kforge-dev@lists.okfn.org',
    license='GPL',
    url='http://www.kforgeproject.com/',
#    download_url = 'http://appropriatesoftware.net/provide/docs/kforge-%s.tar.gz' % __version__,
    description='Enterprise architecture for project hosting',
    long_description =\
"""
KForge provisions project services on-demand and controls access with a robust, role-based, single sign-on access controller.

Project services include version control systems (e.g. Git, Mercurial, Subversion); project frameworks with mechanisms to plan and track work (e.g. Trac); wikis and mailing lists (e.g. MoinMoin, Mailman); and content management systems and blogs (e.g. Joomla, Wordpress).

KForge provides a complete Web interface for review and administration of project members and services, as well as a fully-developed plugin system so that new kinds of services can be added easily.
""",
    classifiers = [
        'Development Status :: 5 - Production/Stable',
        'Environment :: Console',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License (GPL)',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries :: Python Modules'],
)
