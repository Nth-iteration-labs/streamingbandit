# StreamingBandit

Provides a webserver to quickly setup and evaluate possible solutions to contextual multi-armed bandit (cMAB) problems. Allows user to create new "experiments", each with their own policy, and disclose an API to evaluate the policy in applications.

For the documentation see http://mkaptein.github.io/streamingbandit

# Pre-requisites

Python 3.x+ (untested on Python 2.7) with the following packages:
* [Tornado](http://www.tornadoweb.org)
* [Redis-Py](http://redis-py.readthedocs.io/en/latest/)
* [YAML](http://pyyaml.org)
* [PyMongo](http://api.mongodb.com/python/current/)
* [NumPy](http://www.numpy.org)
* [SciPy](http://www.scipy.org)
* [scikit-learn](http://scikit-learn.org/stable/)
* [APScheduler](http://apscheduler.readthedocs.io/)

[Redis](http://redis.io)
[MongoDB](http://www.mongodb.com)

# Installation & Configuration

## Python dependencies for StreamingBandit:

### Mac/Linux
To install all dependencies:

```
sudo python3 setup.py install
```

## Redis
### Mac
To install redis on Mac via _Brew_:
```
brew install redis
```

### Linux
You could look at this tutorial: https://www.digitalocean.com/community/tutorials/how-to-install-and-use-redis

## MongoDB
### Mac
To install MongoDB via _Brew_:
```
brew install mongodb
```

### Linux (ubuntu/debian)
see http://docs.mongodb.org/manual/tutorial/install-mongodb-on-ubuntu/

Configuration file (<root>/app/config.cfg) contains both Redis-server IP and Port as well as the mongo server IP and port. If you run all three on the same host, your good to go with the default settings, otherwise change them to your environment.

# Running streamingbandit 

When everything is configured, do the following:
* Start Redis 
* Start MongoDB 

(Ideally they are automatically started, as they are usally used in a server-context. Look at the links above to find how-to's on starting Redis and MongoDB automatically.)

Then you can start streamingbandit web-server via the terminal:
```
python3 app.py
```
(Note that this would be the simple local testing process, for actual deployment one would need a different approach.)

On your local machine browse to: http://localhost:8080 (which is the default port where Tornado will run)
Then, either browse to:
* http://localhost:8080/reference.html to see the docs or,
* http://localhost:8080/management.html to manage the experiments running on the server.

_Happy Streaming_


