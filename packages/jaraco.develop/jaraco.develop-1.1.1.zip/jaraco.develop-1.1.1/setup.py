# -*- coding: UTF-8 -*-

"""
Setup script for building jaraco.develop

Copyright © 2010 Jason R. Coombs
"""

try:
	from distutils.command.build_py import build_py_2to3 as build_py
except ImportError:
	from distutils.command.build_py import build_py

from setuptools import setup, find_packages
try:
	from jaraco.util.package import read_long_description
	long_description = read_long_description()
except:
	long_description = None

__author__ = 'Jason R. Coombs <jaraco@jaraco.com>'
__version__ = '$Rev: 1718 $'[6:-2]
__svnauthor__ = '$Author: jaraco $'[9:-2]
__date__ = '$Date: 2010-04-08 17:35:22 -0400 (Thu, 08 Apr 2010) $'[7:-2]

name = 'jaraco.develop'

setup (name = name,
		version = '1.1.1',
		description = 'Routines to assist development',
		long_description = long_description,
		author = 'Jason R. Coombs',
		author_email = 'jaraco@jaraco.com',
		url = 'http://pypi.python.org/pypi/'+name,
		packages = find_packages(exclude=['tests']),
		namespace_packages = ['jaraco',],
		scripts = ['scripts/test-python-symlink-patch.py'],
		license = 'MIT',
		classifiers = [
			"Development Status :: 4 - Beta",
			"Intended Audience :: Developers",
			"Programming Language :: Python",
		],
		entry_points = {
			'console_scripts': [
				'apply-python-bug-patch=jaraco.develop:apply_python_bug_patch_cmd',
				],
		},
		install_requires=[
			'jaraco.util',
			'BeautifulSoup',
		],
		extras_require = {
		},
		dependency_links = [
		],
		tests_require=[
			'nose>=0.10',
		],
		test_suite = "nose.collector",
		cmdclass=dict(build_py=build_py),
	)
