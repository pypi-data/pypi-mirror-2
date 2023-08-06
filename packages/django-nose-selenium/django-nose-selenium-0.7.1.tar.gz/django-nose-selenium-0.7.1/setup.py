# -*- coding: utf-8 -*-
"""
django-nose-selenium
~~~~~~~~~~~~~~~~~~~~

A plugin to run selenium smoothly with nose.


:copyright: 2010, Pascal Hartig <phartig@weluse.de>
:license: BSD, see LICENSE for more details
"""

import os
from setuptools import setup
from noseselenium import __version__


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setup(
    name="django-nose-selenium",
    version=__version__,
    author="Pascal Hartig",
    author_email="phartig@weluse.de",
    description="A nose plugin to run selenium tests with django",
    long_description=read('README.rst'),
    url="http://github.com/weluse/django-nose-selenium",
    packages=['noseselenium', 'noseselenium.thirdparty'],
    requires=['Django (>=1.2)', 'nose (>=0.10)'],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 2.6",
        "Topic :: Software Development :: Testing",
        "Topic :: Software Development :: Libraries :: Python Modules"
    ],
    entry_points={
        'nose.plugins.0.10': [
            'selenium = noseselenium.plugins:SeleniumPlugin',
            'selenium_fixtures = noseselenium.plugins:SeleniumFixturesPlugin',
            'cherrypyliveserver = noseselenium.plugins:CherryPyLiveServerPlugin',
            'djangoliveserver = noseselenium.plugins:DjangoLiveServerPlugin'
        ]
    }
)
