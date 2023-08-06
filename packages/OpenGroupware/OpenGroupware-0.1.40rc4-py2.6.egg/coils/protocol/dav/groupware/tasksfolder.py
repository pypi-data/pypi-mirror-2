#
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
from StringIO                          import StringIO
from datetime                          import datetime, timedelta
from coils.foundation                  import CTag
from coils.core                        import Appointment
from coils.net                         import DAVFolder, \
                                                OmphalosCollection, \
                                                OmphalosObject, \
                                                StaticObject, \
                                                Parser, \
                                                Multistatus_Response
from taskobject                        import TaskObject
from rss_feed                          import TasksRSSFeed
from groupwarefolder                   import GroupwareFolder


class TasksFolder(DAVFolder, GroupwareFolder):

    def __init__(self, parent, name, **params):
        DAVFolder.__init__(self, parent, name, **params)
        self._start = None
        self._end   = None

    def get_property_webdav_owner(self):
        return u'<D:href>/dav/Contacts/{0}.vcf</D:href>'.format(self.context.account_id)

    # PROP: resourcetype

    def get_property_webdav_resourcetype(self):
        return '<D:collection/><C:calendar/><G:vtodo-collection/>'

    # PROP: GETCTAG

    def get_property_caldav_getctag(self):
        return self.get_ctag()

    def get_ctag(self):
        if (self.is_collection_folder):
            return self.get_ctag_for_collection()
        else:
            return self.get_ctag_for_entity('Job')

    # PROP: supported-calendar-component-set (RFC4791)

    def get_property_caldav_supported_calendar_component_set(self):
        return unicode('<C:comp name="VTODO"/>')

    def _load_contents(self):
        # TODO: Read range from server configuration
        self.log.info('Loading content in task folder for name {0}'.format(self.name))
        if (self.is_collection_folder):
            result = None
            if (self.is_project_folder):
                result = self.context.run_command('project::get-tasks', project=self.entity)
            if (self.is_favorites_folder):
                # Not supported
                raise NotImplementedException('Favoriting of tasks is not supported.')
            elif (self.name == 'Delegated'):
                result = self.context.run_command('task::get-delegated')
            elif (self.name == 'ToDo'):
                result = self.context.run_command('task::get-todo')
            elif (self.name == 'Assigned'):
                #TODO: Implement assigned tasks
                result = [ ]
            elif (self.name == 'Archived'):
                result = self.context.run_command('task::get-archived')
            if (result is None):
                return False
            else:
                self.data = { }
                if (self._start is None): self._start = datetime.now() - timedelta(days=1)
                if (self._end is None): self._end   = datetime.now() + timedelta(days=90)
                for task in result:
                    if ((self._start is not None) or (self._end is not None)):
                        #TODO: Implement date-range scoping
                        pass
                    self.insert_child(task.object_id, task, alias='{0}.ics'.format(task.object_id))
        else:
            self.insert_child('Delegated', TasksFolder(self, 'Delegated', context=self.context, request=self.request))
            self.insert_child('ToDo',      TasksFolder(self, 'ToDo',      context=self.context, request=self.request))
            self.insert_child('Archived',  TasksFolder(self, 'Archived',  context=self.context, request=self.request))
            self.insert_child('Assigned',  TasksFolder(self, 'Assigned',  context=self.context, request=self.request))
        return True

    def object_for_key(self, name, auto_load_enabled=True, is_webdav=False):
        if (name == '.ctag'):
            if (self.is_collection_folder):
                return self.get_ctag_representation(self.get_ctag_for_collection())
            else:
                return self.get_ctag_representation(self.get_ctag_for_entity('Job'))
        elif ((name == '.json') and (self.load_contents())):
            return self.get_collection_representation(name, self.get_children())
        elif (name == '.content.json'):
            return self.get_collection_representation(name, self.get_children(), rendered=True)
        else:
            location = None
            if (self.is_collection_folder):
                if (self.load_contents() and (auto_load_enabled)):
                    task = self.get_child(name)
                    location = '/dav/Tasks/{0}'.format(name)
            else:
                self.load_contents()
                result = self.get_child(name)
                if (result is not None):
                    return result
                (object_id, payload_format, task, values) = self.get_task_for_key(name)
            if (task is not None):
                return self.get_entity_representation(name, task, location=location,
                                                                   is_webdav=is_webdav)
        self.no_such_path()

    def do_OPTIONS(self):
        ''' Return a valid WebDAV OPTIONS response '''
        methods = [ 'OPTIONS, GET, HEAD, POST, PUT, DELETE, TRACE, COPY, MOVE',
                    'PROPFIND, PROPPATCH, LOCK, UNLOCK, REPORT, ACL' ]
        self.request.simple_response(200,
                                     data=None,
                                     mimetype=u'text/plain',
                                     headers={ 'DAV':           '1, 2, access-control, calendar-access',
                                               'Allow':         ','.join(methods),
                                               'Connection':    'close',
                                               'MS-Author-Via': 'DAV'} )

    def do_REPORT(self):
        ''' Preocess a report request '''
        payload = self.request.get_request_payload()
        self.log.debug('REPORT REQUEST: %s' % payload)
        parser = Parser.report(payload)
        if (parser.report_name == 'calendar-query'):
            self._start = parser.parameters.get('start', None)
            self._end   = parser.parameters.get('end', None)
            if (self.load_contents()):
                resources = [ ]
                for child in self.get_children():
                    if child.caldav_uid is None:
                        name = u'{0}.ics'.format(child.object_id)
                    else:
                        name = child.caldav_uid
                    resources.append(TaskObject(self, name, entity=child,
                                               location='/dav/Tasks/{0}.ics'.format(child.object_id),
                                               context=self.context,
                                               request=self.request))
                stream = StringIO()
                properties, namespaces = parser.properties
                Multistatus_Response(resources=resources,
                     properties=properties,
                     namespaces=namespaces,
                     stream=stream)
                self.request.simple_response(207,
                                             data=stream.getvalue(),
                                             mimetype=u'text/xml; charset=utf-8')
        elif (parser.report_name == 'calendar-multiget'):
            resources = []
            for href in parser.references:
                try:
                    key = href.split('/')[-1]
                    resources.append(self.get_object_for_key(key))
                except NoSuchPathException, e:
                    self.log.debug('Missing resource {0} in collection'.format(key))
                except Exception, e:
                    self.log.exception(e)
                    raise e
                stream = StringIO()
                properties, namespaces = parser.properties
                Multistatus_Response(resources=resources,
                     properties=properties,
                     namespaces=namespaces,
                     stream=stream)
                self.request.simple_response(207,
                                             data=stream.getvalue(),
                                             mimetype=u'text/xml; charset=utf-8')
        else:
            raise CoilsException('Unsupported report {0} in {1}'.format(parser.report_name, self))

    def do_PUT(self, name):
        ''' Process a PUT request '''
        self.log.debug('PUT request with name {0}'.format(name))
        payload = self.request.get_request_payload()
        (object_id, payload_format, task, payload_values) = self.get_task_for_key_and_content(name, payload)
        if_etag = self.request.headers.get('If-Match', None)
        if (if_etag is None):
            self.log.warn('Client issued a put operation with no If-Match!')
        else:
            # TODO: Implement If-Match test
            self.log.warn('If-Match test not implemented at {0}'.format(self.url))
        if (task is None):
            # Create task
            task = self.context.run_command('task::new', values=payload_values)
            task.caldav_uid = name
            self.apply_permissions(task)
            self.context.commit()
            self.request.simple_response(201,
                                         data=None,
                                         mimetype=u'text/calendar; charset=utf-8',
                                         headers={ 'Etag':     u'{0}:{1}'.format(task.object_id, task.version),
                                                   'Location': u'/dav/Tasks/{0}'.format(name) } )
        else:
            if (isinstance(payload_values, list)):
                payload_values = payload_values[0]
            self.context.run_command('task::set', object=task,
                                                  values=payload_values)
            self.context.commit()
            self.request.simple_response(204,
                                         data=None,
                                         mimetype=u'text/calendar; charset=utf-8',
                                         headers={ 'Etag':     u'{0}:{1}'.format(task.object_id, task.version),
                                                   'Location': u'/dav/Tasks/{0}'.format(name) } )
