#!/usr/bin/env python3

# Author: Maurits Kaptein, Jules Kruijswijk.
# contributor: Robin van Emden, Vincent Gijsen
# 
#

from setuptools import setup

setup(name='StreamingBandit',
      	version='2.0',
      	description='Python application to setup and run streaming (contextual) bandit experiments.',
      	author='Maurits Kaptein',
      	author_email='maurits@mauritskaptein.com',
      	url='https://github.com/MKaptein/streamingbandit',
        license='MIT',
      	packages=[],
      	install_requires=[
		'tornado',
		'redis',
		'pyyaml',
		'pymongo',
                'numpy',
                'scipy',
                'scikit-learn',
                'apscheduler'
	]	
     )
