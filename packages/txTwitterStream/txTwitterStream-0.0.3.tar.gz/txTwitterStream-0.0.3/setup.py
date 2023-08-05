#!/usr/bin/env python
# coding: utf-8

from setuptools import setup, find_packages

trove_classifiers=[
    "Development Status :: 4 - Beta",
    "License :: OSI Approved :: BSD License",
    "License :: DFSG approved",
    "Intended Audience :: Developers",
    "Operating System :: OS Independent",
    "Natural Language :: English",
    "Programming Language :: Python",
    "Programming Language :: Python :: 2",
    "Programming Language :: Python :: 2.5",
    "Programming Language :: Python :: 2.6",
    "Topic :: Utilities",
    "Topic :: Software Development :: Libraries",
    ]

setup(
    name="txTwitterStream",
    version="0.0.3",
    description="A fork of Alexandre Fiori's TwistedTwitterStream Twitter client library for the Twitter Streaming API",
    author="Wade Simmons",
    author_email="wade@wades.im",
    url="http://github.com/wadey/txtwitterstream",
    py_modules=["txtwitterstream"],
    packages = find_packages(),
    test_suite="txtwitterstream.test",
    install_requires=["Twisted >= 9.0.0"],
    setup_requires=['setuptools_trial'],
    tests_require=['mock'],
    license = "BSD",
    classifiers=trove_classifiers,
    zip_safe = False, # We prefer unzipped for easier access.
)
