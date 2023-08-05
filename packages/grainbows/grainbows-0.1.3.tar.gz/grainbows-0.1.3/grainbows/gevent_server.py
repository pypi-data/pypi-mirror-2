# -*- coding: utf-8 -
#
# This file is part of grainbows released under the MIT license. 
# See the NOTICE for more information.

import errno
import os


import gevent
from gevent import socket
from gevent.event import Event
from gevent.greenlet import Greenlet
from gevent.pool import Pool
from gevent import select


from gunicorn import arbiter
from gunicorn import util
from grainbows.worker_base import WorkerBase

class GEventWorker(WorkerBase):
            
    def init_process(self):
        super(GEventWorker, self).init_process()
        self.pool = Pool(self.worker_connections)
        self.socket = socket.socket(_sock=self.socket)
        
    def accept(self):
        try:
            client, addr = self.socket.accept()
            self.pool.spawn(self.handle, client, addr)
        except socket.error, e:
            if e[0] not in (errno.EAGAIN, errno.EWOULDBLOCK):
                raise

    def acceptor_loop(self):
        while self.alive:
            self.notify()   
            # If our parent changed then we shut down.
            if self.ppid != os.getppid():
                self.log.info("Parent changed, shutting down: %s" % self)
                return
            
            if self.nb_connections > self.worker_connections:
                continue
                
            try:
                ret = select.select([self.socket], [], self.PIPE, 1)
                if ret[0]:
                    self.accept()
            except select.error, e:
                if e[0] == errno.EINTR:
                    continue
                if e[0] == errno.EBADF:
                    continue
                raise
            except KeyboardInterrupt:
                return
                         
class GEventArbiter(arbiter.Arbiter):
    
    def init_worker(self, worker_age, pid, listener, app, timeout, conf):
        return GEventWorker(worker_age, pid, listener, app, timeout, conf)