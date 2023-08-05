#!/usr/bin/python

from setuptools import setup, find_packages

import os
lines = open(os.path.join(os.path.dirname(__file__), 'README')).read().strip().splitlines()

sdesc = lines[0]
ldesc = '\n'.join(lines[1:])

setup(name='hgspellcheck',
	version='1.0rc2',
	author='Iain Lowe',
	author_email='me@ilowe.net',
	description=sdesc,
	long_description=ldesc,
	py_modules=['hgspellcheck'],
	license='MIT',
	zip_safe=True,
	url='http://bitbucket.org/ilowe/hgspellcheck',
	download_url='http://bitbucket.org/ilowe/hgspellcheck/downloads',
	keywords='mercurial hg scm spelling spellcheck spellchecker',
	install_requires = ['pyenchant>=1.5.3'],
)
