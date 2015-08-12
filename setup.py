#!/usr/bin/env python

# Author: Maurits Kaptein, et al.
# contributor: Vincent Gijsen
# 
#

from setuptools import setup

setup(name='StreamingBandid',
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
		'pymongo',
		'json'
	]	
     )
