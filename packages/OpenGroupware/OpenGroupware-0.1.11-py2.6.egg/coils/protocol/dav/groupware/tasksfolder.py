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
import datetime, pprint
from coils.foundation                  import CTag
from coils.core                        import Appointment
from coils.protocol.dav.foundation     import DAVFolder, \
                                                OmphalosCollection, \
                                                OmphalosObject
from taskobject                        import TaskObject


class TasksFolder(DAVFolder):
    def __init__(self, parent, name, **params):
        DAVFolder.__init__(self, parent, name, **params)

    # PROP: GETCTAG

    def get_property_unknown_getctag(self):
        return self.get_property_caldav_getctag()

    def get_property_webdav_getctag(self):
        return self.get_property_caldav_getctag()

    def get_property_caldav_getctag(self):
        return self.get_ctag()

    def get_ctag(self):
        ''' Return a ctag appropriate for this object.
            Actual WebDAV objects should override this method '''
        db = self.context.db_session()
        query = db.query(CTag).filter(CTag.entity=='Job')
        ctags = query.all()
        if (len(ctags) == 0):
            return None
        query = None
        return ctags[0].ctag

    def _get_task_for_key(self, key):
        object_id = int(str(key).split('.')[0])
        a = self.context.run_command('task::get', id=object_id)
        return a

    def _load_self(self):
        # TODO: Read range from server configuration
        self.log.info('Loading content in task folder for name {0}'.format(self.name))
        result = None
        if (self.name == 'Tasks'):
            self.data = { 'Delegated': [ TasksFolder(self, 'Delegated', context=self.context, request=self.request) ],
                          'ToDo':      [ TasksFolder(self, 'ToDo', context=self.context, request=self.request) ],
                          'Archived':  [ TasksFolder(self, 'Archived', context=self.context, request=self.request) ],
                          'Assigned':  [ TasksFolder(self, 'Assigned', context=self.context, request=self.request) ] }
            return True
        elif (self.name == 'Delegated'):
            result = self.context.run_command('task::get-delegated')
        elif (self.name == 'ToDo'):
            result = self.context.run_command('task::get-todo')
        elif (self.name == 'Assigned'):
            result = self.context.run_command('task::get-assigned')
        elif (self.name == 'Archived'):
            result = self.context.run_command('task::get-archived')
        if (result is not None):
            self.data = { }
            for task in result:
                self.data['{0}.ics'.format(task.object_id)] = [ task ]
            return True
        return False

    def object_for_key(self, name):
        if (self.load_self()):
            if (self.name == 'Tasks'):
                # Is a request in the ROOT task folder
                if ((name == 'Delegated') or
                    (name == 'ToDo') or
                    (name == 'Archived') or
                    (name == 'Assigned')):
                    return self.data[name][0]
                else:
                    task = self._get_task_for_key(name)
                    if (task is not None):
                        if (name[-5:] == '.json'):
                            return OmphalosObject(self,
                                                   name,
                                                   entity=task,
                                                   context=self.context,
                                                   request=self.request)
                        else:
                            return TaskObject(self, name, entity=self.data[name][0],
                                                           context=self.context,
                                                           request=self.request)
            else:
                # Request in SUBFOLDER
                if (name == '.json'):
                    return OmphalosCollection(self,
                                               name,
                                               data=self.data.values(),
                                               context=self.context,
                                               request=self.request)
                elif (name == '.content.json'):
                    return OmphalosCollection(self,
                                               name,
                                               rendered=True,
                                               detail=0,
                                               data=self.data.values(),
                                               context=self.context,
                                               request=self.request)
                elif ((name[-4:] == '.ics') or (name[-5:] == '.json')):
                    task = self._get_task_for_key(name)
                    if (task is not None):
                        if (name[-5:] == '.json'):
                            # Return JSON presentaion
                            return OmphalosObject(self,
                                                   name,
                                                   entity=task,
                                                   context=self.context,
                                                   request=self.request)
                        else:
                            # Default to ICS presentation
                            # Returns a redirect to the root tasks folder
                            return TaskObject(self,
                                                name,
                                                entity=task,
                                                location='/dav/Tasks/{0}'.format(name),
                                                context=self.context,
                                                request=self.request)
        self.no_such_path()
