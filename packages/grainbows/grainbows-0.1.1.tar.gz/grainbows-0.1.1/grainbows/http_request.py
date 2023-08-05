# -*- coding: utf-8 -
#
# This file is part of gunicorn released under the MIT license. 
# See the NOTICE for more information.

import os
import socket
import select
from grainbows import __version__
from gunicorn.http import Request

class KeepaliveEOF(Exception):
    pass

class GRequest(Request):
    
    SERVER_VERSION = "grainbows/%s" % __version__
    
    def read(self):
        ret = select.select([self._sock], [], [], self.conf.keepalive)
        if not ret[0]:
            return
        try:
            return super(GRequest, self).read()
        except socket.error, e:
            if e[0] == 54:
                return
            raise