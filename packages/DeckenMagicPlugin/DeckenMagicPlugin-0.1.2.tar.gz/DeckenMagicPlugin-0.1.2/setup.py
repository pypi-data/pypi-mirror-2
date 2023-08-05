#import ez_setup
#ez_setup.use_setuptools()
from setuptools import setup


setup(
	name='DeckenMagicPlugin',
	version='0.1.2',
	#scripts = ['magicplugin.py', 'conjunto.py', 'ez_setup.py'],
	package_data={'' : ['*.csv',], 'images' : 'images/back.jpg' },
	install_requires=["BeautifulSoup"],
	entry_points = {
		'decken.cards_plugin' : [
			'magic = magicplugin:MagicPlugin'
		]
	},
	
	author='Claudio Torcato',
	author_email='claudiotorcato@gmail.com',
	description='Decken Plugin to Trade Card Game Magic: the Gathering',
	license="PSF",
	keywords = "tcg mtg magic deck card python gnome linux mac n800",
)