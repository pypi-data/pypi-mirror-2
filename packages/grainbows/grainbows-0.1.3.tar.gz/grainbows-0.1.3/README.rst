About
-----

grainbow 'Green Rainbows' is a WSGI HTTP Server for UNIX, for sleepy application. It's based on `Gunicorn`_ but it's designed to handle applications that expect long request/response times and/or slow clients. For other applications, you should use gunicorn, since it's easier to debug.

Features
========

* Designed for `WSGI <http://www.python.org/dev/peps/pep-0333/>`_
* Built on `Gunicorn`_, inheriting its process/socket management features such as transparent upgrades and Python configuration DSL.
* Decode chunked transfers on-the-fly, allowing upload progress notifications or
  stream-based protocols over HTTP
* Support for `Eventlet`_ and `Gevent`_ .


Applications
============

* Websockets (see `example <http://github.com/benoitc/grainbows/blob/master/examples/websocket.py>`_), see the `demo <http://vimeo.com/10111929>`_
* Reverse proxy implementation (with `Restkit WSGI proxy <http://benoitc.github.com/restkit/wsgi_proxy.html>`_)
* Comet
* Long Polling
* ...

Install
=======

Grainbows requires Python 2.x superior to 2.5.

Install from sources::

    $ python setup.py install

Or from Pypi::

  $ easy_install -U grainbows

  
By default grainbows use `Gunicorn`_ arbiter, so you won't have any benefits. You need to install `Eventlet`_ or  `Gevent`_ to use concurrency features.

do::

  $ easy_install -U eventlet

Replace `eventlet` by **gevent** if you want to use `gevent`.
  
  
Usage
=====

for WSGI application:
+++++++++++++++++++++

To launch the `example application <http://github.com/benoitc/grainbows/blob/master/examples/websocket.py>`_ packaged with Grainbows::

    $ cd /path/to/grainbows/examples/
    $ grainbows websocket:app
    
and then go on `http://localhost:8000` to see the result.

*Note* : by default the configuration is set to use eventlet. If you want to test with gevent, edit `grainbows.conf.py` file and replace `use="eventlet"` by `use="gevent"`.

The module ``test_keepalive:app`` specifies the complete module name and WSGI callable. You can replace it with anything that is available on your ``PYTHONPATH`` like such::

    $ cd ~/
    $ grainbows -c /path/to/configfile.py awesomeproject.wsgi.main:main_app
    

Full command line usage::

  $ grainbows --help
  Usage: grainbows [OPTIONS] APP_MODULE

  Options:
    --use=USE             method to use (eventlet, gevent)
    -c CONFIG, --config=CONFIG
                          Config file. [none]
    -b BIND, --bind=BIND  Adress to listen on. Ex. 127.0.0.1:8000 or
                          unix:/tmp/gunicorn.sock
    -w WORKERS, --workers=WORKERS
                          Number of workers to spawn. [1]
    -p PIDFILE, --pid=PIDFILE
                          set the background PID FILE
    -D, --daemon          Run daemonized in the background.
    -m UMASK, --umask=UMASK
                          Define umask of daemon process
    -u USER, --user=USER  Change worker user
    -g GROUP, --group=GROUP
                          Change worker group
    -n PROC_NAME, --name=PROC_NAME
                          Process name
    --log-level=LOGLEVEL  Log level below which to silence messages. [info]
    --log-file=LOGFILE    Log to a file. - equals stdout. [-]
    -d, --debug           Debug mode. only 1 worker.
    --version             show program's version number and exit
    -h, --help            show this help message and exit
  

For `Django <http://www.djangoproject.com>`_ applications use the `grainbows_django` command line and for `Paste <http://pythonpaste.org>`_ compatible applications (`Pylons`_, `TurboGears 2`_, ...) use `grainbows_paste`. See the `usage <http://gunicorn.org/usage.html>`_ page on Gunicorn website for more information.

    

Configuration file
++++++++++++++++++

A configuration file is needed to setup `Grainbows` specific settings. An example can be found `here <http://github.com/benoitc/grainbows/blob/master/examples/grainbows.conf.py>`_ ::

  use = "eventlet"
  worker_connections = 1000
  
You can also configure other settings, see the `Gunicorn configuration <http://gunicorn.org/configuration.html>`_ page for more details.

Development
===========

You can get the source on `Github <http://github.com>`_ : 

  http://github.com/benoitc/grainbows/
  
And send your feedback on `the tracker <http://github.com/benoitc/grainbows/issues>`_ .
  

.. _Gunicorn: http://gunicorn.org
.. _Eventlet: http://eventlet.net
.. _Gevent: http://gevent.org
.. _Pylons: http://pylonshq.com/
.. _Turbogears 2: http://turbogears.org/2.0/

