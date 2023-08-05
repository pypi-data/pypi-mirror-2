#!/usr/bin/python
from glob import glob
import os
import ez_setup
ez_setup.use_setuptools()
from setuptools import setup, find_packages

setup(
	name='Decken',
	version='0.1.5',
	install_requires=["BeautifulSoup"],
	package_data = {'decken': ['maginbook2.glade']},
	packages = find_packages(),
	#entry_points = {
	#	'gui_scripts' : [ 'decken=decken_script:command']
	#},
	scripts = ['decken_script'],
	
	
	author='Claudio Torcato',
	author_email='claudiotorcato@gmail.com',
	description='Deck Organizer to Trading Card Games',
	license="PSF",
	keywords = "tcg mtg magic deck card python gnome linux mac n800"
)