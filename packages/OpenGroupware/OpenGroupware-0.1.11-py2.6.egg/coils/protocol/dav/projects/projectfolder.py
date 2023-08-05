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
from coils.protocol.dav.foundation     import DAVFolder
from coils.protocol.dav.foundation     import EmptyFolder
from documentsfolder                   import DocumentsFolder
from notesfolder                       import NotesFolder
from tasksfolder                       import TasksFolder


class ProjectFolder(DAVFolder):
    def __init__(self, parent, name, **params):
        DAVFolder.__init__(self, parent, name, **params)

    def _load_self(self):
        return True

    def keys(self):
        return [ 'Tasks', 'Notes', 'Contacts', 'Documents', 'Enterprises', 'Versions' ]

    def object_for_key(self, name):
        if (name == 'Documents'):
            folder = self.context.run_command('project::get-root-folder', project=self.entity)
            if (folder is None):
                self.no_such_path()
            return DocumentsFolder(self, name,
                                    entity=folder,
                                    request=self.request,
                                    context=self.context)
        elif (name == 'Notes'):
            return NotesFolder(self, name,
                                entity=self.entity,
                                request=self.request,
                                context=self.context)
        elif (name == 'Tasks'):
            return TasksFolder(self, name,
                                entity=self.entity,
                                request=self.request,
                                context=self.context)
        else:
            return EmptyFolder(self, name,
                                entity=self.entity,
                                request=self.request,
                                context=self.context)