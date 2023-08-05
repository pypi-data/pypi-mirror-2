from setuptools import setup

setup(name="lpaste",
	version="0.0.1",
	packages=['lpaste'],
	entry_points = {
		'console_scripts': [
			'lpaste = lpaste.lpaste:main',
		],
	},
	install_requires = [
		'poster', 
	],
)

