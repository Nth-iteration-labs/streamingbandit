#!/usr/bin/env python3

# Author: Maurits Kaptein, Jules Kruijswijk.
# contributor: Robin van Emden, Vincent Gijsen

from setuptools import setup

setup(name='StreamingBandit',
    version='1.0.2',
    description='Python application to setup and run streaming (contextual) bandit experiments.',
    author='Nth-iteration',
    author_email='maurits@mauritskaptein.com',
    url='https://github.com/nth-iteration-labs/streamingbandit',
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
    'apscheduler',
    'bcrypt'
    ])
