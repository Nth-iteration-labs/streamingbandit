#!/usr/bin/env python3

# Author: Maurits Kaptein, Jules Kruijswijk.
# contributor: Vincent Gijsen
# 
#

from setuptools import setup

setup(name='StreamingBandit',
      	version='0.1',
      	description='Python application to setup and run streaming (contextual) bandit experiments.',
      	author='Maurits Kaptein',
      	author_email='',
      	url='https://github.com/MKaptein/streamingbandit',
      	packages=[],
      	install_requires=[
		'tornado',
		'redis',
		'PyYAML',
		'pymongo'
	]	
     )
