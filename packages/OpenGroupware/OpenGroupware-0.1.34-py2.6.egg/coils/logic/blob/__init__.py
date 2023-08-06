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
#
from get_blob             import GetBLOB                  # blob::get
from get_note             import GetNote                  # note::get
from get_drawer           import GetDrawer                # drawer::get
from get_document         import GetDocument              # document::get
from get_folder           import GetFolder                # folder::get
from get_handle           import GetDocumentHandle, \
                                  GetNoteHandle
from create_note          import CreateNote               # note::new
from update_note          import UpdateNote               # note::set
from delete_note          import DeleteNote               # note::delete
from create_document      import CreateDocument           # document::new
from create_version       import CreateVersion            # document::new-version
from ls                   import ListFolder               # folder:ls
from get_note_as_vjournal import GetNoteAsVJournal        # note::get-as-vjournal
from accessmanager        import FolderAccessManager, \
                                  DocumentAccessManager, \
                                  NoteAccessManager
