# Copyright (c) 2009 Adam Tauno Williams <awilliam@whitemice.org>
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
#
import io
from datetime           import datetime
# Core
from coils.core         import *
from coils.net          import *
# DAV Classses
from coils.protocol.dav.foundation     import *

class SignalObject(DAVObject):
    ''' Represent a BPML markup object in WebDAV '''

    def __init__(self, parent, name, **params):
        DAVObject.__init__(self, parent, name, **params)

    def do_GET(self):
        ''' Handle a GET request. '''
        print self.parameters
        #TODO: Interpret URL variables, this object is used to signal the process; this can wake
        # a parked process allowing user interaction with a workflow via simple URLs.
        self.request.send_response(201, 'OK')
        self.request.send_header('Content-Type', 'text/plain')
        self.request.end_headers()
