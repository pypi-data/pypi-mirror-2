import ez_setup
ez_setup.use_setuptools()
from setuptools import setup

setup(
	name='Decken',
	version='0.1',
	scripts = ['decken.py', 'decken_n800.py', 'ez_setup.py'],
	package_data={'' : ['*.csv', '*.glade'], 'images' : [ '*.jpg' ] },
	install_requires=["BeautifulSoup"],
	entry_points = {
		'gui_scripts' : [
			'decken = decken:command'
		]
	},
		
	author='Claudio Torcato',
	author_email='claudiotorcato@gmail.com',
	description='Deck Organizer to Trading Card Games',
	license="PSF",
	keywords = "tcg mtg magic deck card python gnome linux mac n800",
)