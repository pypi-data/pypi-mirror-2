# -*- coding: utf-8 -
#
# This file is part of grainbows released under the MIT license. 
# See the NOTICE for more information.

import errno
import os
import select
import socket

from gunicorn.worker import Worker
from gunicorn import util
from gunicorn import http
from gunicorn.http.tee import UnexpectedEOF

from grainbows import http_response, http_request

ALREADY_HANDLED = object()

class WorkerBase(Worker):
    """ base worker class """
    
    def __init__(self, *args, **kwargs):
        Worker.__init__(self, *args, **kwargs)
        self.nb_connections = 0
        self.worker_connections = self.conf.worker_connections

    def acceptor_loop(self):
        raise NotImplementedError

    def handle(self, client, addr):
        self.nb_connections += 1
        try:
            while True:
                req = http_request.GRequest(client, addr, self.address, self.conf)
                try:
                    environ = req.read()
                    # this should proably be better to have it in gunicorn
                    if not environ or not req.parser.headers:
                        return
                    response = self.app(environ, req.start_response)
                    if response == ALREADY_HANDLED:
                        break
                except Exception, e:
                    #Only send back traceback in HTTP in debug mode.
                    if not self.debug:
                        raise
                    util.write_error(client, traceback.format_exc())
                    break 

                http_response.GResponse(client, response, req).send()
                if req.parser.should_close:
                    break
        except socket.error, e:
            if e[0] != errno.EPIPE:
                self.log.exception("Error processing request.")
            else:
                self.log.warn("Ignoring EPIPE")
        except UnexpectedEOF:
            self.log.exception("remote closed the connection unexpectedly.")
        except Exception, e:
            self.log.exception("Error processing request.")
            try:            
                # Last ditch attempt to notify the client of an error.
                mesg = "HTTP/1.0 500 Internal Server Error\r\n\r\n"
                util.write_nonblock(client, mesg)
            except:
                pass
        finally:   
            self.nb_connections -= 1 
            util.close(client)
            
    def run(self):
        self.init_process()
        self.acceptor_loop()