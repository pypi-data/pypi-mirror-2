#import ez_setup
#ez_setup.use_setuptools()
from setuptools import setup, find_packages


setup(
	name='DeckenMagicPlugin',
	version='0.1.4',
	#scripts = ['magicplugin.py', 'conjunto.py', 'ez_setup.py'],
	package_data={'deckenmagicplugin' : ['*.csv', 'images/back.jpg']  },
	packages = find_packages(),
	install_requires=["BeautifulSoup"],
	entry_points = {
		'decken.cards_plugin' : [
			'magic = deckenmagicplugin.magicplugin:MagicPlugin'
		]
	},
	
	author='Claudio Torcato',
	author_email='claudiotorcato@gmail.com',
	description='Decken Plugin to Trade Card Game Magic: the Gathering',
	license="PSF",
	keywords = "tcg mtg magic deck card python gnome linux mac n800",
)