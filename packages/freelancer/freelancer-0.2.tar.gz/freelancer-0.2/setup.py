#!/usr/bin/env python
from setuptools import setup, find_packages

setup(name="freelancer",
      version="0.2",
      description="API Library for freelancer.com",
      author="E. Cooper",
      author_email="strangerthanus@gmail.com",
      url="http://github.com/ecooper/python-freelancer",
      packages = find_packages(),
      install_requires = ['httplib2', 'oauth2'],
      entry_points="""
      # -*- Entry points: -*-
      [console_scripts]
      freelancer=freelancer.cli:main
      """,
      license = "GNU General Public License v3")
