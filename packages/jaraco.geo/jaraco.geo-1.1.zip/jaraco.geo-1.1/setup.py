# -*- coding: UTF-8 -*-

""" Setup script for building jaraco-util distribution

Copyright © 2004-2010 Jason R. Coombs
"""

try:
	from distutils.command.build_py import build_py_2to3 as build_py
except ImportError:
	from distutils.command.build_py import build_py

from setuptools import setup, find_packages

__author__ = 'Jason R. Coombs <jaraco@jaraco.com>'
__version__ = '$Rev: 1759 $'[6:-2]
__svnauthor__ = '$Author: jaraco $'[9:-2]
__date__ = '$Date: 2010-04-14 08:39:16 -0400 (Wed, 14 Apr 2010) $'[7:-2]

name = 'jaraco.geo'

setup (
	name = name,
	version = '1.1',
	description = 'Geographic coordinates package',
	long_description = open('docs/index.txt').read(),
	author = 'Jason R. Coombs',
	author_email = 'jaraco@jaraco.com',
	url = 'http://pypi.python.org/pypi/'+name,
	packages = find_packages(),
	include_package_data=True,
	namespace_packages = ['jaraco',],
	license = 'MIT',
	zip_safe=False,
	classifiers = [
		"Development Status :: 4 - Beta",
		"Intended Audience :: Developers",
		"Programming Language :: Python",
	],
	entry_points = {
		'console_scripts': [
			],
	},
	install_requires=[
		'jaraco.util',
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
