# -*- coding: UTF-8 -*-

""" Setup script for building jaraco-util distribution

Copyright © 2004-2010 Jason R. Coombs
"""

from setuptools import setup, find_packages

__author__ = 'Jason R. Coombs <jaraco@jaraco.com>'
__version__ = '$Rev: 1752 $'[6:-2]
__svnauthor__ = '$Author: jaraco $'[9:-2]
__date__ = '$Date: 2010-04-13 15:26:31 -0400 (Tue, 13 Apr 2010) $'[7:-2]

name = 'jaraco.geo'

setup (
	name = name,
	version = '1.0',
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
)
