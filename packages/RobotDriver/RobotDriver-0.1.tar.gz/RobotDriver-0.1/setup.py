#!/usr/bin/env python
from setuptools import setup, find_packages

setup(
    name = 'RobotDriver',
    version = '0.1',
    description = 'RobotFramework suport for Bitten',
    long_description = '''
RobotDriver is a Trac__ plugin that adds RobotFramework__ support
to Bitten__.

__ http://trac.edgewall.org
__ http://code.google.com/p/robotframework
__ http://bitten.edgewall.org
''',
    author = 'Xie Yanbo',
    author_email = 'xieyanbo@gmail.com',
    packages = find_packages(),
    package_data = {
        'robotdriver': ['templates/*.html'],
    },
    entry_points = {
        'trac.plugins': [
            'robotdriver.robot = robotdriver.robot',
            ],
        'bitten.recipe_commands': [
            'http://bitbucket.org/xyb/robotdriver#robot = '
            'robotdriver.robot:robot',
            ],
    },
    zip_safe = False,
    url = 'http://bitbucket.org/xyb/robotdriver',
    keywords = 'trac,bitten,robotframework,pybot,test',
    install_requires = [
        'trac==0.11.2',
        'bitten>=0.6b2',
        'robotframework>=2.5',
        ],
    classifiers = [
        'Programming Language :: Python',
        'Operating System :: OS Independent',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
    ],
)
