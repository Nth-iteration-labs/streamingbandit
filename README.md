streamingbandit
========

Development of streaming solutions to contextual bandit problem in Python

Pre-requisites
==============

- Python 3.x+ with the following packages:
-- Tornado
-- json
-- redis
-- yaml
-- mongo

- Redis 2.8+

Installation & Configuration
============================

A nice way to install the missing packages is to use easy_install or pip.
See the Python website for a detailed how-to.
Redis has to be installed using command-line or the Redis website.

Configuration file only contains Redis-server IP and Port. If you run this on your own machine, keep default settings, which are "localhost" and 6379.

Running streampy 
================

When everything is configured, run Redis via the terminal (redis-server).
Then you can start streamingbandit via the terminal (python streamingbandit).

To-do list
==========
(see issues. Quite a lot actually).
