# -*- coding: utf-8 -
#
# This file is part of grainbow released under the MIT license. 
# See the NOTICE for more information.

import gunicorn.config
import os

class Config(gunicorn.config.Config):
    
    DEFAULT_CONFIG_FILE = 'grainbows.conf.py'
    
    DEFAULTS = dict(
        backlog=2048,
        bind='127.0.0.1:8000',
        daemon=False,
        debug=False,
        default_proc_name = os.getcwd(),
        group=None,
        keepalive=2,
        logfile='-',
        loglevel='info',
        pidfile=None,
        proc_name = None,
        timeout=30,
        tmp_upload_dir=None,
        umask="0",
        user=None,
        use="base",
        workers=None,
        worker_connections=1000,
        
        after_fork=lambda server, worker: server.log.info(
            "Worker spawned (pid: %s)" % worker.pid),
        
        before_fork=lambda server, worker: True,

        before_exec=lambda server: server.log.info("Forked child, reexecuting")
    )
       
    @property   
    def workers(self):
        if not self.conf.get('workers'):
            if self.conf.get('use') in ('gevent', 'eventlet'):
                workers = 12
            else:
                workers = 1
        else:            
            workers = int(self.conf["workers"])
            if not workers:
                raise RuntimeError("number of workers < 1")
        if self.conf['debug'] == True: 
            workers = 1
        return workers
    
    @property
    def arbiter(self):
        if self.conf['use'] == "base":
            from gunicorn.arbiter import Arbiter
            return Arbiter
        if self.conf['use'] == "eventlet":
            import eventlet
            if eventlet.version_info < (0,9,7):
                raise RuntimeError("You need eventlet >= 0.9.7")
            from grainbows.eventlet_server import patch_eventlet
            patch_eventlet()
            eventlet.monkey_patch(all=True, os=False)
            
            from grainbows.eventlet_server import EventletArbiter as Arbiter
            
        elif self.conf['use'] == "gevent":
            from gevent import monkey
            monkey.patch_all(thread=True,  ssl=True)
            from grainbows.gevent_server import GEventArbiter as Arbiter
        return Arbiter