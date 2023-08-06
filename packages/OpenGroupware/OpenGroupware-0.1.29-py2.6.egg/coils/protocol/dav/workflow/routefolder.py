#
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
from signalobject                      import SignalObject
from proplistobject                    import PropertyListObject
from workflow                          import WorkflowPresentation

class RouteFolder(DAVFolder, WorkflowPresentation):
    def __init__(self, parent, name, **params):
        DAVFolder.__init__(self, parent, name, **params)
        self.entity = params['entity']
        self.route_id = self.entity.object_id

    def supports_PUT(self):
        return True

    def _load_contents(self):
        self.data = { }
        self.log.debug('Returning enumeration of processes of route {0}.'.format(self.name))
        processes = self.context.run_command('route::get-processes', id=self.route_id)
        for process in processes:
            self.insert_child(str(process.object_id), ProcessFolder(self,
                                                                    str(process.object_id),
                                                                    parameters=self.parameters,
                                                                    entity=process,
                                                                    context=self.context,
                                                                    request=self.request))
        self.insert_child('markup.xml', BPMLObject(self,
                                                   'markup.xml',
                                                   entity=self.entity,
                                                   context=self.context,
                                                   request=self.request))
        self.insert_child('Versions', VersionsFolder(self,
                                                     'Versions',
                                                     entity=self.entity,
                                                     context=self.context,
                                                     request=self.request))
        self.insert_child('propertyList.txt', PropertyListObject(self,
                                                                 'propertyList.txt',
                                                                 entity=self.entity,
                                                                 context=self.context,
                                                                 request=self.request))
        return True

    def object_for_key(self, name, auto_load_enabled=True, is_webdav=False):
        self.log.debug('Request for folder key {0}'.format(name))
        if (name == 'signal'):
            return SignalObject(self, name,
                                 parameters=self.parameters,
                                 entity=self.entity,
                                 context=self.context,
                                 request=self.request)
        elif (self.load_contents()):
            if (self.has_child(name)):
                return self.get_child(name)
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
                process = self.create_process(route=self.entity, data=payload, priority=201)
                if (len(self.parameters) > 0):
                    for key, value in self.parameters.items():
                        key = 'xattr_{0}'.format(key.lower().replace(' ', ''))
                        if value is None:
                            value = 'YES'
                        elif (len(value) > 0):
                            value = str(value[0])
                        self.context.property_manager.set_property(process,
                                                                   'http://www.opengroupware.us/oie',
                                                                   key, value)
                self.context.commit()
                self.log.info('Process {0} created via DAV PUT by {1}.'\
                    .format(process.object_id, self.context.get_login()))
                message = self.get_input_message(process)
                self.start_process(process)
                self.context.run_command('process::start', process=process)
            except Exception, e:
                self.log.exception(e)
                raise CoilsException('Failed to create process')
            paths = self.get_process_urls(process)
            self.request.send_response(301, 'Moved')
            self.request.send_header('Location', paths['self'])
            self.request.send_header('Content-Type', message.mimetype)
            self.request.send_header('X-COILS-WORKFLOW-MESSAGE-UUID', message.uuid)
            self.request.send_header('X-COILS-WORKFLOW-MESSAGE-LABEL', message.label)
            self.request.send_header('X-COILS-WORKFLOW-PROCESS-ID', process.object_id)
            self.request.send_header('X-COILS-WORKFLOW-OUTPUT-URL', paths['output'])
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
