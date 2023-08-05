#!/usr/bin/env python

from setuptools import setup, find_packages
version='0.1'

setup(name='django-queries',
		version=version,
		description='Generic query interface for django models',
		author='Peter Guthy',
		author_email='peter@guthy.at',
		url='http://code.google.com/p/django-queries/',
		classifiers=[
			"Development Status :: 4 - Beta",
			"Environment :: Web Environment",
			"Framework :: Django",
			"Intended Audience :: Developers",
			"License :: OSI Approved :: BSD License",
			"Programming Language :: Python",
			"Topic :: Database :: Front-Ends",
			"Topic :: Software Development :: Libraries :: Python Modules",
			],
		license="BSD",
		packages=find_packages(),
		package_dir={'queries':'queries'},
		package_data={'queries': [
			'templates/queries/*.html',
			'locale/*/LC_MESSAGES/django.*',
			'media/css/*',
			'media/img/admin/*',
			'media/js/*.js',
			'media/js/admin/*.js',
			]},
		long_description="""
		With this application, you can create easily admin-like query interfaces for your django models.

		You can define the fields which the user can search for. The entered search criteria are chained together with AND and the results are displayed.
		""",
		include_package_data=True,
		)
