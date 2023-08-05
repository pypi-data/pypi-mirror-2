# Copyright (c) 2010 Tauno Williams <awilliam@whitemice.org>
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
import urllib
from coils.protocol.dav.foundation     import DAVFolder
from documentobject                    import DocumentObject

class DocumentsFolder(DAVFolder):
    def __init__(self, parent, name, **params):
        DAVFolder.__init__(self, parent, name, **params)

    def _load_self(self):
        self.data = { }
        contents = self.context.run_command('folder::ls', id=self.entity.object_id)
        for entity in contents:
            if (entity.__entityName__ == 'Folder'):
                self.data[entity.file_name] = entity
            elif (entity.__entityName__ == 'File'):
                self.data['{0}.{1}'.format(entity.file_name, entity.extension)] = entity
        return True

    def object_for_key(self, name):
        if  (self.load_self()):
            if (name in self.data):
                if (self.data[name].__entityName__ == 'Document'):
                    return DocumentObject(self, name, entity=self.data[name],
                                                       request=self.request,
                                                       context=self.context)
                elif (self.data[name].__entityName__ == 'Folder'):
                    return DocumentsFolder(self, name, entity=self.data[name],
                                                        request=self.request,
                                                        context=self.context)
        self.no_such_path()
