#!/usr/bin/env python

from distutils.core import setup

setup(name='metroclient',
    version = '0.93',
    author = 'Evan Hazlett',
    author_email = 'support@lumentica.com',
    packages = ['metroclient'],
    description = 'AppHosted application deployment utility',
    url = 'http://apphosted.com',
    license = 'License :: OSI Approved :: GNU General Public License (GPL)',
    long_description = """
    Metro is the application deployment utility for managing and deploying web applications
    hosted on http://apphosted.com""",
    download_url = 'http://metro.apphosted.com/client/get/',
    scripts = ['metro'],
    install_requires = ['pycurl'],
    platforms = [
        "All",
        ],
    classifiers = [
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.5",
        "Development Status :: 4 - Beta",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: GNU General Public License (GPL)",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Topic :: Software Development",
        "Topic :: Software Development :: Build Tools",
        "Topic :: Utilities",
        ]
    )

