#!/usr/bin/env python
"""Setup script for upicasa"""
from setuptools import setup

setup(
    name="upicasa",
    version="0.2",
    description="A command line uploader for PicasaWeb",
    long_description=file("README").read(),
    author="Albertas Agejevas",
    author_email="alga@pov.lt",
    py_modules=['upicasa'],
    install_requires = [
        "gdata",
        ],
    entry_points = {'console_scripts': ['upicasa = upicasa:main']},
    keywords = "picasaweb google picasa upload",
    classifiers = [
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Intended Audience :: End Users/Desktop',
        'License :: OSI Approved :: GNU General Public License (GPL)',
        'Programming Language :: Python',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Topic :: Internet :: WWW/HTTP :: Site Management',
        'Topic :: Multimedia :: Graphics',
        'Topic :: Utilities'],
    )
