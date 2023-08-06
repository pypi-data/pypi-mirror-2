# -*- coding: utf-8 -*-
#!/usr/bin/env python

from distutils.core import setup
VERSION = '0.1.2'

setup(name='django-jquery-widgets',
	version=VERSION,
	description='jQuery-powered widgets and fields for Django',
	long_description=open('README').read(),
	author='Sindre Røkenes Myren',
	author_email='smyrman@gmail.com',
	license='BSD',
	url='http://github.com/smyrman/django-jquery-widgets',
	install_requires='django >= 1.1',
	download_url='http://github.com/smyrman/django-jquery-widgets/tarball/%s'%VERSION,
	packages=['jquery_widgets'],
	package_data={'jquery_widgets': ['media/js/*.js', 'media/css/*.css',
		'templates/jquery_widgets/*.html']},
)
