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
import os
from tempfile                          import mkstemp
from coils.core                        import *
from coils.protocol.dav.foundation     import DAVFolder
from routefolder                       import RouteFolder
from utility                           import compile_bpml
from signalobject                      import SignalObject
from workflow                          import WorkflowPresentation

class RoutesFolder(DAVFolder, WorkflowPresentation):
    def __init__(self, parent, name, **params):
        DAVFolder.__init__(self, parent, name, **params)

    def supports_PUT(self):
        return True

    def _load_self(self):
        self.data = { }
        if (self.name == 'Routes'):
            # Implemented
            self.log.debug('Returning enumeration of available routes.')
            routes = self.context.run_command('route::get')
            for route in routes:
                self.data[route.name] = route
        else:
            return False
        return True

    def object_for_key(self, name):
        if (name == 'signal'):
            return SignalObject(self, name,
                                 parameters=self.parameters,
                                 entity=None,
                                 context=self.context,
                                 request=self.request)
        elif (self.load_self()):
            if (name in self.data):
                return RouteFolder(self,
                                    name,
                                    parameters=self.parameters,
                                    entity=self.data[name],
                                    context=self.context,
                                    request=self.request)
        raise self.no_such_path()

    def do_PUT(self, request_name):
        """ Allows routes to be created by dropping BPML documents into /dav/Routes """
        _temp_file  = mkstemp(prefix='Coils.', suffix='.bpml')
        _wfile      = os.fdopen(_temp_file[0], "w")
        _filename   = _temp_file[1]
        _wfile.write(self.request.get_request_payload())
        _wfile.close()
        self.log.debug('Stored potential BPML in {0}'.format(_filename))
        description, cpm = compile_bpml(_filename, log=self.log)
        try:
            route = self.context.run_command('route::new', values=description, filename=_filename)
        except Exception, e:
            self.log.exception(e)
            raise CoilsException('Route creation failed.')
        self.context.commit()
        self.request.send_response(301, 'Moved')
        self.request.send_header('Location', '/dav/Workflow/Routes/{0}/markup.xml'.format(route.name))
        self.request.send_header('Content-Type', 'text/xml')
        #self.request.send_header('Content-Length', str(len(route.get_markup())))
        self.request.end_headers()
        #w.flush()
