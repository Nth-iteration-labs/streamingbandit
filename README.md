# streamingbandit

Provides a webserver to quickly setup and evaluate possible solutions to contextual multi-armed bandit problems. Allows user to create new "experiments", each with their own policy, and disclose an API to evaluate the policy in applications.

For the documentation see http://mkaptein.github.io/streamingbandit

# Pre-requisites

Python 3.x+ (although 2.7 seems to work) with the following packages:
* Tornado
* json
* redis
* yaml (PYYamel)
* mongo
* Redis 2.8+

# Installation & Configuration

## Python dependencies for StreamingBandit:

### Mac/Linux
To install all dependencies:

```
sudo python setup.py install
```
### Windows
run (as administrator?):
```
python setup.py install
``` 


## Redis
### Mac
to install redis on Mac via _Brew_
```
brew install redis
```

### Linux
You could look at this tutorial: https://www.digitalocean.com/community/tutorials/how-to-install-and-use-redis

## MongoDB
### Mac
To install Brew via _Brew_
```
brew install mongodb
```

### Linux (ubuntu/debian)
see http://docs.mongodb.org/manual/tutorial/install-mongodb-on-ubuntu/

Configuration file (<root>/app/config.cfg) contains both Redis-server IP and Port as well as the mongo server IP and port. If you run all three on the same host, your good to go with the default settings, otherwise change them to your environment

# Running streamingbandit 

When everything is configured, do the following:
* Start redis (using redis-server command)
* Start mongodb (using mongod command)

(idealy they are automagically started, as they are usally used in a server-context)

Then you can start streamingbandit web-server via the terminal (using python app.py). (note that this would be the simple local testing process, for actual deployment one would need a different approach).

On your local machine browse to: http://localhost:8080 (which is the default port where Tornado will run)
Then, either browse to:
* http://localhost:8080/reference.html to see the docs or,
* http://localhost:8080/management.html to manage the experiments running on the server.

# To-do list
(see issues).

# Developing javascript 
We use some build tools to manage javascript. In order to generate your own, please use these steps:

install npm on your computer

```
npm install grunt 
npm install bower

```
after which you can run the command: ```grunt``` when present in the root folder

This wil download all javascript libraries and minify our own.


_Happy Streaming_


