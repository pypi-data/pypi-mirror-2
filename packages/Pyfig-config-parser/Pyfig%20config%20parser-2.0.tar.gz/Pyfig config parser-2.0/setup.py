# Pyfig setup.py
from distutils.core import setup
setup(
	name = "Pyfig config parser",
	version = "2.0",
	description = "Very small and simple configuration file parser",
	author = "Alec Henriksen", 
	author_email = "alecwh@gmail.com",
	url = "http://pyfig.alecwh.com/",
	py_modules = ['pyfig'],
	download_url = "http://bitbucket.org/alecwh/pyfig/downloads/pyfig2.0.tar.gz",
	keywords = ['configuration', 'parser', 'config', 'config parser'],
	classifiers = [
		'Programming Language :: Python',
		'Programming Language :: Python :: 3',
		'Development Status :: 5 - Production/Stable',
		'Intended Audience :: Developers',
		'License :: OSI Approved :: GNU General Public License (GPL)',
		'Operating System :: OS Independent',
		'Topic :: Software Development',
		'Topic :: Software Development :: Libraries :: Python Modules',
		
		],
	long_description = """\
Pyfig: A simple config file parser for python
=============================================

Information:

* Project by Alec Henriksen <alecwh@gmail.com>
* License: GNU GPL
* Website: http://pyfig.alecwh.com/
* Version: 2.0 (09/27/2009)
* Development: http://bitbucket.org/alecwh/pyfig/


Features
--------

* Easy to use (straightforward, simple)
* Supports categories/sections in the config file
* Supports comments
* Very robust in terms of parsing
* One file, no package


More information/usage examples @ http://pyfig.alecwh.com/
----------------------------------------------------------
"""

)
