streamingbandit
========

Provides a webser to quickly setup and evaluate possible solutions to contextual multi-armed bandit problems. Allows user to create new "experiments", each with their own policy, and disclose an API to evaluate the policy in applications.

Pre-requisites
==============

- Python 3.x+ with the following packages:
-- Tornado
-- json
-- redis
-- yaml
-- mongo
-- Redis 2.8+

Installation & Configuration
============================

A nice way to install the missing packages is to use easy_install or pip.
See the Python website for a detailed how-to.
Redis has to be installed using command-line or the Redis website.
Mongo needs to be installed similarly.

Configuration file (config.cfg) contains both Redis-server IP and Port as well as the mongo server IP and port. If you run this on your own machine, keep default settings, which are "localhost" and 6379 and 27017 respectively.

Running streamingbandit 
================

When everything is configured, do the following:
- Start redis (using redis-server command)
- Start mongo (using mongod command)

Then you can start streamingbandit server via the terminal (using python app.py). (note that this would be the simple local testing process, for actual deployment one would need a different approach).

On you local machine browse to: http://localhost:8080 (which is the default port where Tornado will run)
Then, either browse to:
- http://localhost:8080/reference.html to see the docs or,
- http://localhost:8080/management.html to manage the experiments running on the server.

To-do list
==========
(see issues).
