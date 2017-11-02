************
Installation
************

We offer two ways of using StreamingBandit. If you want the smoothest and easiest experience, we recommend to look at `Install in Docker`_.

Install in Docker
=================

Using `Docker`_ you can easily install StreamingBandit in an isolated container and will have you up and running within a matter of minutes. Docker is a virtualization framework that uses separate containers for each piece of software that you are using. Every dependency and installation procedure is handled by Docker. This is the easiest and recommended way to run StreamingBandit. For more information about `Docker`_, check out their website.

After you have installed Docker and have it up and running, you can get StreamingBandit started using the following commands (note that you also need `Git`_)::

    $ git clone https://github.com/nth-iteration-labs/streamingbandit
    $ cd streamingbandit
    $ docker-compose up -d

After the Docker containers are up and running, we can add an admin account with password 'test' so that you can login to the back-end::

    $ docker exec -t streamingbandit_web_1 python3 ../insert_admin.py -p test

Stopping and starting the containers can be done by::

    $ docker-compose stop
    $ docker-compose start

.. Note:: You can also stop the Docker containers using ``$ docker-compose down``, but use this with caution, as it will destroy the containers and also all your saved progress and data!

The last few commands will only start up the back-end. If you would like to have the front-end running as well, you can accomplish that using the following commands::

    $ docker-compose -f docker-compose.yml -f docker-compose.front-end.yml up -d

Then starting and stopping can be done by issuing::

    $ docker-compose -f docker-compose.yml -f docker-compose.front-end.yml stop
    $ docker-compose -f docker-compose.yml -f docker-compose.front-end.yml start

.. Note:: The front-end will be taken from an existing image from the `Dockerhub`_ and thus you will not need to download a Git repository.

Install and running from Source
===============================

Installing from Source
----------------------

Currently this section is only for Mac/Linux and only Python 3 is supported. Firstly, you will have to install all the Python dependencies::

    $ pip3 install .

Redis
^^^^^

We use Redis for its speed to store our parameters.

Mac
"""
To install Redis on Mac, we can use brew::

    $ brew install redis

Linux
"""""
To install Redis on Linux and have it running as a daemon from start-up, check out this tutorial on `DigitalOcean`_.

MongoDB
^^^^^^^

We use MongoDB for all logging and archiving.

Mac
"""
To install MongoDB on Mac, we can again use brew::

    $ brew install mongodb

Linux (Ubuntu/Debian)
"""""""""""""""""""""
To install MongoDB on Linux (Ubuntu/Debian) and have it running as a daemon from start-up, check out the tutorial on the official website `MongoDB`_. For other distributions there are similar tutorials.

Configurating Redis and MongoDB locations
-----------------------------------------

If you have a Redis and MongoDB instance running on other systems (e.g. different Amazon clusters) than you are running StreamingBandit on, you can change the IP and port in the config file (/app/config.cfg).

Running StreamingBandit
-----------------------

If everything is correctly configured:
* Start Redis
* Start MongoDB

Then you can start the StreamingBandit back-end by issuing the following commands::

    $ cd streamingbandit/app
    $ python3 app.py

You can now go to ``http://localhost:8080/`` and if everything is running correctly, you will see a welcome page!

Using StreamingBandit front-end
-------------------------------

To use StreamingBandit more intuitively, you can use our front-end (`StreamingBandit-ui`_) as well. 

Just follow these steps.

1. Download and unzip the StreamingBanditUI package [here](https://github.com/Nth-iteration-labs/streamingbandit-ui/releases/download/v1.0/StreamingBanditUI.zip), if you haven't already. 
The StreamingBanditUI package will extract into a folder called StreamingBanditUI in the same directory that you downloaded StreamingBanditUI.zip
2. Upload the all of the files contained in the StreamingBanditUI folder to the desired location on your web server and visit index.html.

OR

2. Run StreamingBanditUI by clicking on index.html in the StreamingBanditUI directory. This works in most, but not all browsers. Recent versions of Firefox, Microsoft Edge and Google Chrome should work fine.
3. Now enter the IP or domain together with the port on StreamingBandit is running (default: http://localhost:8080) and login to the StreamingBandit server.

That's it! You should now be able to access your StreamingBandit server, and start experimenting!


.. _Docker: http://docs.docker.io/
.. _Dockerhub: https://hub.docker.com/
.. _Git: https://git-scm.com/
.. _DigitalOcean: https://www.digitalocean.com/community/tutorials/how-to-install-and-use-redis
.. _MongoDB: https://docs.mongodb.com/manual/tutorial/install-mongodb-on-ubuntu/
.. _StreamingBandit-ui: https://github.com/nth-iteration-labs/streamingbandit-ui
