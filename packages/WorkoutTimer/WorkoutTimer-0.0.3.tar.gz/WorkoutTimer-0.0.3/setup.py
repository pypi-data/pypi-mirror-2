from distutils.core import setup
	
setup(
	name='WorkoutTimer',
	version='0.0.3',
	author='Jesse OBrien',
	author_email='jobrien@drivendaily.org',
	url='http://www.drivendaily.org',
	packages=['WorkoutTimer'],
	license='license.txt',
	description='Interval-based workout timer which allows for difficulty changes',
	long_description=open('README.txt').read(),
)
