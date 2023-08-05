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
from coils.net              import *
from foundation             import DAVFolder, DAVObject, EmptyFolder
# DAV content providers
from groupware              import ContactsFolder, CalendarFolder, AccountsFolder, \
                                    TeamsFolder, TasksFolder
from projects               import ProjectsFolder, CabinetsFolder
from files                  import FilesFolder
from workflow               import WorkflowFolder

DAV_ROOT_FOLDERS = { 'Contacts'     : 'ContactsFolder',
                     'Projects'     : 'ProjectsFolder',
                     'Calendar'     : 'CalendarFolder',
                     'Journal'      : 'EmptyFolder',
                     'Collections'  : 'EmptyFolder',
                     'Files'        : 'FilesFolder',
                     'Cabinets'     : 'CabinetsFolder',
                     'Users'        : 'AccountsFolder',
                     'Tasks'        : 'TasksFolder',
                     'Teams'        : 'TeamsFolder',
                     'Workflow'     : 'WorkflowFolder' }

class DAVRoot(DAVFolder, Protocol):
    '''The root of the DAV hierarchy.'''
    __pattern__   = 'dav'
    __namespace__ = None
    __xmlrpc__    = False

    def __init__(self, parent, **params):
        DAVFolder.__init__(self, parent, 'dav', **params)
        DAVFolder.Root = self
        #print self.user_agent

    def get_name(self):
        return 'dav'

    def keys(self):
        ''' Returns the containers objects (children), this is an array of strings. '''
        self.init_context()
        return DAV_ROOT_FOLDERS.keys()

    def object_for_key(self, name):
        ''' Return the object for the named key, this is expected to be a DAV object. '''
        self.init_context()
        if (DAV_ROOT_FOLDERS.has_key(name)):
            classname = DAV_ROOT_FOLDERS[name]
            classclass = eval(classname)
            x = classclass(self, name, parameters=self.parameters,
                                       request=self.request,
                                       context=self.context)
            return x
        # Throw a 404 (Not Found) exception
        self.no_such_path()