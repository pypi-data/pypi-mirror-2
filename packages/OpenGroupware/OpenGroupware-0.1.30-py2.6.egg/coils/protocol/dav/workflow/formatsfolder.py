# Copyright (c) 2010 Adam Tauno Williams <awilliam@whitemice.org>
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
import os, yaml
from tempfile                          import mkstemp
from coils.core                        import *
from coils.protocol.dav.foundation     import DAVFolder
from coils.logic.workflow              import Format
from formatobject                      import FormatObject

class FormatsFolder(DAVFolder):
    def __init__(self, parent, name, **params):
        DAVFolder.__init__(self, parent, name, **params)

    def supports_PUT(self):
        return True

    def _load_contents(self):
        self.data = { }
        if (self.name == 'Formats'):
            for name in Format.ListFormats():
                self.insert_child('{0}.yaml'.format(name), Format.Load(name))
        else:
            return False
        return True

    def object_for_key(self, name, auto_load_enabled=True, is_webdav=False):
        if (self.load_contents()):
            if (self.has_child(name)):
                return FormatObject(self,
                                     name,
                                     entity=self.get_child(name),
                                     context=self.context,
                                     request=self.request)
        self.no_such_path()

    def do_PUT(self, request_name):
        """ Allows formats to be created by dropping YAML documents into /dav/Workflow/Formats """
        try:
            payload = self.request.get_request_payload()
            format = self.context.run_command('format::new', yaml=payload)
        except Exception, e:
            self.log.exception(e)
            raise CoilsException('Format creation failed.')
        self.context.commit()
        if (format.get_name() != request_name[:-5]):
            self.request.send_response(301, 'Moved')
            self.request.send_header('Location', '/dav/Workflow/Formats/{0}.yaml'.format(format.get_name()))
        else:
            self.request.send_response(201, 'OK')
            self.request.end_headers()
