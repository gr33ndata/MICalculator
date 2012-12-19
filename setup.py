from distutils.core import setup

setup(
	name='Mutual Information Calculator',
	version='0.1.0',
	author='Tarek Amr',
	author_email='',
	packages=['mutualinfo'],
	license='LICENSE.txt',
	description='Calculates the mutual information for data, to determine best classification features.',
	long_description=open('README.txt').read(),
)
