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
from coils.protocol.dav.foundation     import DAVFolder, DAVObject
from coils.protocol.dav.foundation     import DAVFolder
from coils.protocol.dav.foundation     import EmptyFolder
from coils.protocol.dav.foundation     import OmphalosCollection
from coils.protocol.dav.foundation     import OmphalosObject
from projectfolder                     import ProjectFolder
from rss_feed                          import ProjectTaskActionsRSSFeed

class ProjectsFolder(DAVFolder):
    ''' Provides a WebDAV collection containing all the projects (as
        subfolders) which the current account has access to,'''

    def __init__(self, parent, name, **params):
        DAVFolder.__init__(self, parent, name, **params)

    def _load_self(self):
        ''' Enumerates projects using account::get-projects.'''
        self.data = { }
        content = self.context.run_command('account::get-projects')
        if (content is not None):
           for project in content:
               self.data[project.number] = [ project ]
        else:
            return False
        return True

    def keys(self):
        if (self.load_self()):
            return self.data.keys()
        return []

    def _get_project_for_key(self, key):
        if (self.data is not None):
            if (key in self.data):
                return self.data[key]
        try:
            object_id = int(str(key).split('.')[0])
        except:
            return None
        return self.context.run_command('project::get', id=object_id)

    def object_for_key(self, name):
        if ((name == '.json') and (self.load_self())):
            # Get an index of the folder as an Omphalos collection
            return OmphalosCollection(self,
                                       name,
                                       data=self.data.values(),
                                       context=self.context,
                                       request=self.request)
        elif ((name[-5:] == '.json') or
              (name[-4:] == '.xml') or
              (name[-5:] == '.yaml')):
            # Get a project in Omphalos representation
            entity = self._get_project_for_key(name)
            if (entity is not None):
               return OmphalosObject(self,
                                      name,
                                      entity=entity,
                                      context=self.context,
                                      request=self.request)
        elif (name == 'actions.rss'):
            # Task actions RSS feed
            return ProjectTaskActionsRSSFeed(self, name, None,
                                              request=self.request,
                                              context=self.context)
        elif (name in self.get_children()):
           # WebDAV collection
            print 'project folder has name!'
            x = self.data[name][0]
            x = ProjectFolder(self, x.number,
                              entity=x,
                              request=self.request,
                              context=self.context)
            return x
        elif (('(' in name) or (')' in name)):
            name = name.replace('(', '%28').replace(')', '%29')
            return self.object_for_key(name)
        self.no_such_path()
