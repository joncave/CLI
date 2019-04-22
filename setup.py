#!/usr/bin/env python

PROJECT = 'Faction CLI'

# Change docs/sphinx/conf.py too!
VERSION = '2019.04.21'

from setuptools import setup, find_packages

try:
    long_description = open('README.rst', 'rt').read()
except IOError:
    long_description = ''

setup(
    name=PROJECT,
    version=VERSION,

    description='Console application for interacting with Faction',
    long_description=long_description,

    author='The Faction Team',
    author_email='team@factionc2.com',

    url='https://github.com/factionc2/cli/',
    download_url='https://github.com/factionc2/cli/tarball/master',

    platforms=['Any'],

    scripts=[],

    provides=[],
    install_requires=['cliff'],

    namespace_packages=[],
    packages=find_packages(),
    include_package_data=True,

    entry_points={
        'console_scripts': [
            'faction = factioncli.main:main'
        ],
        'faction.cli': [
            'setup = factioncli.commands.setup:Setup',
            'start = factioncli.commands.faction:Start',
            'stop = factioncli.commands.faction:Stop',
            'restart = factioncli.commands.faction:Restart',
            'reset = factioncli.commands.faction:Reset',
            'clean = factioncli.commands.clean:Clean',
            'status = factioncli.commands.status:Status',
            'new = factioncli.commands.new:New'
        ]
    },

    zip_safe=False,
)