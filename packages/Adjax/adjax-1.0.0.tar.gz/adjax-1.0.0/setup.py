#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import ez_setup
ez_setup.use_setuptools()

from setuptools import setup, find_packages
setup(
    name = "Adjax",
    version = "1.0",
    packages = find_packages(exclude=["website*", "tests*", "design*"]),
    url = 'http://adjax.hardysoftware.com.au/',
    install_requires = ['django>=1.0'],
    author = "Will Hardy",
    author_email = "adjax@hardysoftware.com.au",
    description = "A framework for easing the development of Django sites with Ajax.",
    license = "New BSD",
    keywords = "ajax, django, framework",
    package_data = {
        'adjax': ['media/js/*.js'],
        }

)

