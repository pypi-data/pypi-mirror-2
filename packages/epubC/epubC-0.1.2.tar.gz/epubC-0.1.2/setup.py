#!/usr/bin/env python

from distutils.core import setup

setup(
	name = "epubC",
	version = "0.1.2",
	description = ".epub file creator",
	author = "Awad Mackie",
	author_email = "firesock.serwalek@gmail.com",
	py_modules = ["epubC"],
	license = "GPLv3",
	url = "http://pypi.python.org/pypi/epubC",
	long_description = """\
	epubC.py - .epub file creator
	=============================

	Library to create .epub files according to idpf standards.

	- Requires lxml - checked with 2.2.6
	- Works with Python 3.1.2""",
	classifiers = [
		"Development Status :: 3 - Alpha",
		"Environment :: Other Environment",
		"Intended Audience :: Developers",
		"License :: OSI Approved :: GNU General Public License (GPL)",
		"Operating System :: OS Independent",
		"Programming Language :: Python",
		"Programming Language :: Python :: 3",
		"Topic :: Software Development :: Libraries :: Python Modules"],
	keywords = ["epub", "ebook"]
	)
