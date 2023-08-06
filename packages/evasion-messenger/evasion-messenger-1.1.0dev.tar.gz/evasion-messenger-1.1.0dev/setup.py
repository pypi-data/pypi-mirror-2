"""
Project's setuptool configuration.

This should eggify and in theory upload to pypi without problems.

Oisin Mulvihill
2008-12-23

"""
from setuptools import setup, find_packages

Name='evasion-messenger'
ProjecUrl="http://github.com/oisinmulvihill/evasion-messenger/tarball/master#egg=evasion_messenger"
Version='1.1.0dev'
Author='Oisin Mulvihill'
AuthorEmail='oisinmulvihill at gmail dot com'
Maintainer=' Oisin Mulvihill'
Summary='Messaging library used to package and delivery events'
License='Evasion Project CDDL License'
ShortDescription=Summary
Description=Summary

TestSuite = 'evasion.messenger.tests'

needed = [
    'simplejson',
    'stomper',
    'pydispatcher',
]

import sys
if not sys.platform.startswith('win'):
    needed.append('twisted==8.2.0')

# Include everything under viewpoint. I needed to add a __init__.py
# to each directory inside viewpoint. I did this using the following
# handy command:
#
#  find lib/director/viewpoint -type d -exec touch {}//__init__.py \;
#
# If new directories are added then I'll need to rerun this command.
#
EagerResources = [
    'evasion',
]

ProjectScripts = [
]

PackageData = {
    '': ['*.*'],
}

setup(
    url=ProjecUrl,
    name=Name,
    zip_safe=False,
    version=Version,
    author=Author,
    author_email=AuthorEmail,
    description=ShortDescription,
    long_description=Description,
    license=License,
    test_suite=TestSuite,
    scripts=ProjectScripts,
    install_requires=needed,
    packages=find_packages('lib'),
    package_data=PackageData,
    package_dir = {'': 'lib'},
    eager_resources = EagerResources,
    namespace_packages = ['evasion'],
)
