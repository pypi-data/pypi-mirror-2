#!/usr/bin/python

import sys, os

__author__ = 'Luis Carlos Cruz <carlitos.kyo@gmail.com>'
__version__ = '0.4'

# Distutils version
METADATA = dict(
    name = "mtweets",
    version = __version__,
    py_modules = ['mtweets/__init__',
                  'mtweets/api',
                  'mtweets/utils',
                  'mtweets/streaming'],
    author = 'Luis Carlos Cruz',
    author_email = 'carlitos.kyo@gmail.com',
    description = 'An easy (and up to date) way to access Twitter data with Python.',
    license = 'MIT License',
    url = 'http://github.com/carlitux/mtweets',
    keywords = 'twitter search api tweet twython mtweets',
)

# Setuptools version
SETUPTOOLS_METADATA = dict(
    install_requires = ['setuptools', 'simplejson', 'oauther'],
    include_package_data = True,
    classifiers = [
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Communications :: Chat',
        'Topic :: Internet',
    ]
)

def Main():
    try:
        import setuptools
        METADATA.update(SETUPTOOLS_METADATA)
        setuptools.setup(**METADATA)
    except ImportError:
        import distutils.core
        distutils.core.setup(**METADATA)

if __name__ == '__main__':
    Main()
