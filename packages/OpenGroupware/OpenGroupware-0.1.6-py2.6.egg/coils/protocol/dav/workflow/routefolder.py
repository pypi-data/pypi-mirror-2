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
from coils.core                        import *
from coils.protocol.dav.foundation     import *
from processfolder                     import ProcessFolder
from bpmlobject                        import BPMLObject
from versionsfolder                    import VersionsFolder

class RouteFolder(DAVFolder):
    def __init__(self, parent, name, **params):
        DAVFolder.__init__(self, parent, name, **params)
        self.entity = params['entity']
        self.route_id = self.entity.object_id

    def supports_PUT(self):
        return True

    def _load_self(self):
        self.data = { }
        self.log.debug('Returning enumeration of processes of route {0}.'.format(self.name))
        processes = self.context.run_command('route::get-processes', id=self.route_id)
        for process in processes:
            self.data[str(process.object_id)] = ProcessFolder(self,
                                                               str(process.object_id),
                                                               entity=process,
                                                               context=self.context,
                                                               request=self.request)
        self.data['markup.xml'] = BPMLObject(self, 'markup.xml',
                                             entity=self.entity,
                                             context=self.context,
                                             request=self.request)
        self.data['Versions'] = VersionsFolder(self, 'Versions',
                                               entity=self.entity,
                                               context=self.context,
                                               request=self.request)
        return True

    def object_for_key(self, name):
        self.log.debug('Request for folder key {0}'.format(name))
        if (self.load_self()):
            if (name in self.data):
                return self.data[name]
        self.no_such_path()

    def do_PUT(self, request_name):
        payload = self.request.get_request_payload()
        if (request_name in ['markup.xml', 'markup.bpml']):
            self.context.run_command('route::set', object=self.entity, markup=payload)
            self.context.commit()
            self.request.send_response(201, 'OK')
            self.request.end_headers()
        else:
            self.log.debug('Attempting to create new process from route {0}'.format(self.route_id))
            try:
                process = self.context.run_command('process::new',
                                                   values={'route_id': self.route_id,
                                                           'data': payload})
                self.context.commit()
                self.log.info('Process {0} created via DAV PUT by {1}.'.format(process.object_id, self.context.get_login()))
                message = self.context.run_command('process::get-input-message', process=process)
                self.context.run_command('process::start', process=process)
            except Exception, e:
                self.log.exception(e)
                raise CoilsException('Failed to create process')
            my_path = '{0}/{1}/input'.format(self.get_path()[1:], process.object_id)
            output_path = '{0}/{1}/output'.format(self.get_path()[1:], process.object_id)
            self.request.send_response(301, 'Moved')
            self.request.send_header('Location', my_path)
            self.request.send_header('Content-Type', message.mimetype)
            self.request.send_header('X-COILS-WORKFLOW-MESSAGE-UUID', message.uuid)
            self.request.send_header('X-COILS-WORKFLOW-MESSAGE-LABEL', message.label)
            self.request.send_header('X-COILS-WORKFLOW-PROCESS-ID', process.object_id)
            self.request.send_header('X-COILS-WORKFLOW-OUTPUT-URL', output_path)
            self.request.end_headers()

    def do_DELETE(self):
        # Terminate a process, or delete a completed process
        try:
            self.context.run_command('route::delete', object=self.entity)
            self.commit()
        except:
            self.request.send_response(500, 'Deletion failed')
        else:
            self.request.send_response(204, 'No Content')
        self.request.end_headers()
