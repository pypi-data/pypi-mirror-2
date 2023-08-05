# -*- coding: utf-8 -
#
# This file is part of grainbows released under the MIT license. 
# See the NOTICE for more information.

import errno

import collections
import eventlet
from eventlet.green import os
from eventlet.green import socket
from eventlet.green import select
from eventlet import greenio
from eventlet.hubs import trampoline

from gunicorn import util
from gunicorn import arbiter
from grainbows.worker_base import WorkerBase

__original_GreenPipe__ = greenio.GreenPipe

class _GreenPipe(__original_GreenPipe__):

    def tell(self):
        return self.fd.tell()

    def seek(self, offset, whence=0):
        fd = self.fd
        self.read()
        fd.seek(offset, whence)

_eventlet_patched = None
def patch_eventlet():
    global _eventlet_patched
    if _eventlet_patched:
        return
    greenio.GreenPipe = _GreenPipe
    _eventlet_patched = True
        
class EventletWorker(WorkerBase):

    def init_process(self):
        super(EventletWorker, self).init_process()
        if hasattr(self.socket, 'sock'):
            self.socket.sock.fd.setblocking(0)
            
        self.pool = eventlet.GreenPool(self.worker_connections)
  
    def accept(self):
        try:
            client, addr = self.socket.accept()
            self.pool.spawn_n(self.handle, client, addr)
        except socket.error, e:
            if e[0] in (errno.EWOULDBLOCK, errno.EAGAIN):
                return
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
                ret = select.select([self.socket], [], [], 1)
                if ret[0]:
                    self.accept()
            except select.error, e:
                if e[0] == errno.EINTR:
                    continue
                if e[0] == errno.EBADF:
                    continue
                raise
            

class EventletArbiter(arbiter.Arbiter):
        
    def init_worker(self, worker_age, pid, listener, app, timeout, conf):
        return EventletWorker(worker_age, pid, listener, app, timeout, conf)