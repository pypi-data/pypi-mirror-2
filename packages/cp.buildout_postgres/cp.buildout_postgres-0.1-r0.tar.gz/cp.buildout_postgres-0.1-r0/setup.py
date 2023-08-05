#!/usr/bin/env python
#
# Copyright (c) 2007 Thomas Lotze
# See also LICENSE.txt

"""zc.buildout recipes for setting up a Postgres Environment.
"""

import os.path
import glob

from setuptools import setup, find_packages


project_path = lambda *names: os.path.join(os.path.dirname(__file__), *names)


entry_points = {
    "zc.buildout": [
    "postgres = cp.buildout_postgres.postgres:Recipe",
    "root = cp.buildout_postgres.root:Recipe",
    ],
    }

longdesc = open(project_path("README.txt")).read()

data_files = [("", glob.glob(project_path("*.txt")))]

install_requires = [
    "setuptools",
    "zc.buildout",
    "gocept.cmmi",
	"cns.recipe.symlink"
    ]

extras_require = {
    "test": ["zope.testing"],
    }

classifiers = [
    "Development Status :: 3 - Alpha",
    "Environment :: Console",
    "Environment :: Plugins",
    "Framework :: Buildout",
    "Intended Audience :: Developers",
    "Intended Audience :: System Administrators",
    "License :: OSI Approved :: Zope Public License",
    "Operating System :: OS Independent",
    "Programming Language :: Python",
    "Topic :: Software Development :: Build Tools",
    "Topic :: System :: Software Distribution",
    ]

setup(name="cp.buildout_postgres",
      version="0.1",
      description=__doc__.strip(),
      long_description=longdesc,
      keywords="buildout zc.buildout recipe postgres database server instance",
      classifiers=classifiers,
      author="Craig Sawyer",
      author_email="csawyer@yumaed.org",
      url="http://pypi.python.org/pypi/cp.buildout_postgres",
      license="ZPL 2.1",
      packages=find_packages(),
      namespace_packages=["cp"],
      entry_points=entry_points,
      test_suite="cp.buildout_postgres.tests.test_suite",
      install_requires=install_requires,
      extras_require=extras_require,
      include_package_data=True,
      data_files=data_files,
      zip_safe=True,
      )
