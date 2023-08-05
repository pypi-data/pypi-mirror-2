# -*- coding: utf-8 -
#
# This file is part of grainbows released under the MIT license. 
# See the NOTICE for more information.


from gunicorn.http import response
from gunicorn.util import http_date, write, write_chunk

class GResponse(response.Response):
    
    def send(self):
        if self.req.parser.should_close:
            connection_hdr = "close"
        else:
            connection_hdr = "keep-alive"
        
        # send headers
        resp_head = [
            "HTTP/1.1 %s\r\n" % self.status,
            "Server: %s\r\n" % self.SERVER_VERSION,
            "Date: %s\r\n" % http_date(),
            "Connection: %s\r\n" % connection_hdr
        ]
        resp_head.extend(["%s: %s\r\n" % (n, v) for n, v in self.headers])
        write(self._sock, "%s\r\n" % "".join(resp_head))

        for chunk in self.data:
            if chunk == "": break
            write(self._sock, chunk, self.chunked)
            
        if self.chunked:
            write_chunk(self._sock, "")
            
        if hasattr(self.data, "close"):
            self.data.close()

