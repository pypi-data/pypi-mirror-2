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
import os
from sqlalchemy import *
from coils.core import *
from coils.core.logic import GetCommand


class GetDocumentHandle(GetCommand):
    __domain__ = "document"
    __operation__ = "get-handle"

    def run(self, **params):
        filename = None
        db = self._ctx.db_session()
        query = db.query(Document).filter(Document.object_id.in_(self.object_ids))
        document = query.first()
        if (document.project_id is not None):
            # TODO: We have to use the project type to determine the correct
            # mechanism for constructing the path to the BLOB; for now we are
            # assuming a SKYfs [DB} project.
            filename = '{0}{1}'.format(Backend.store_root(),
                                       document.skyfs_path_to_version(document.version))
        else:
            # TODO: Implement!  How do we locate non-project documents???
            filename = None
        if (filename is not None):
            if (os.path.exists(filename)):
                self._result = open(filename, 'rb')
                self.log.debug('Opened file {0} for reading.'.format(filename))
                return
            else:
                raise CoilsException('BLOB does not exist at path {0}'.format(filename))
        raise CoilsException('Unable to determine path to document.')


class GetNoteHandle(GetCommand):
    __domain__ = "note"
    __operation__ = "get-handle"

    def run(self, **params):
        filename = None
        db = self._ctx.db_session()
        query = db.query(Note).filter(Note.object_id.in_(self.object_ids))
        note = query.first()
        filename = '{0}{1}'.format(Backend.store_root(), note.get_path())
        if (filename is not None):
            self._result = open(filename, 'rb')
            self.log.debug('Opened file {0} for reading.'.format(filename))
            return
        raise CoilsException('Unable to determine path to note.')
