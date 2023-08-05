#!/usr/bin/python
from glob import glob
import os
import ez_setup
ez_setup.use_setuptools()
from setuptools import setup, find_packages

setup(
	name='Decken',
	version='0.2.2',
	install_requires=["BeautifulSoup==3.1.0"],
	package_data = {'decken': ['*.glade']},
	packages = find_packages(),
	#entry_points = {
	#	'gui_scripts' : [ 'decken=decken_script:command']
	#},
	scripts = ['bin/decken_script', 'bin/decken_n800'],
	
	
	author='Claudio Torcato',
	author_email='claudiotorcato@gmail.com',
	description='Deck Organizer to Trading Card Games',
	long_description= open('README.txt').read(),
	license='LICENSE.txt',
	keywords = "tcg mtg magic deck card python gnome linux mac n800"
)