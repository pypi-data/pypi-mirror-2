#!/usr/bin/python

from setuptools import setup, find_packages

setup(name='hgspellcheck',
	version='1.0rc1',
	author='Iain Lowe',
	author_email='me@ilowe.net',
	description='Hook and extension to spellcheck Mercurial commit messages',
	long_description="""
To check all commits for spelling mistakes, and interactively edit them when
they occur, add the extension to the "extensions" section of your .hgrc.

  [extensions]
  hgspellcheck=

To reject all inbound commits that have spelling mistakes, add the hook
on "pretxnchangegroup".

  [hooks]
  # Reject all inbound changesets with spelling errors in their commit
  # messages
  pretxnchangegroup = python:hgspellcheck.hook
  
  # Refuse to create changesets in the local repository if their commit
  # messages contain spelling errors; this works for any commands that
  # create changesets (e.g. commit, qnew, qrecord)
  pretxncommit = python:hgspellcheck.hook
	""".strip(),
	py_modules=['hgspellcheck'],
	license='MIT',
	zip_safe=True,
	url='http://bitbucket.org/ilowe/hgspellcheck/downloads',
	keywords='mercurial hg scm spelling spellcheck spellchecker',
	install_requires = ['pyenchant>=1.5.3'],
)
