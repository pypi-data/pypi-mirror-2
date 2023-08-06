#!/usr/bin/python
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
from coils.core import EntityAccessManager

class FolderAccessManager(EntityAccessManager):
    #TODO: Implement!
    __entity__ = 'Folder'

    def __init__(self, ctx):
        #print 'FolderAccessManager'
        EntityAccessManager.__init__(self, ctx)

    def implied_rights(self, objects):
        # TODO: Implement
        #        Permissions via assignment
        rights = { }
        for entity in objects:
            rights[entity] = set()
            rights[entity].add('r')
            rights[entity].add('w')
        return rights


class FileAccessManager(EntityAccessManager):
    #TODO: Implement!
    __entity__ = 'File'

    def __init__(self, ctx):
        #print 'DocumentAccessManager'
        EntityAccessManager.__init__(self, ctx)

    def implied_rights(self, objects):
        # TODO: Implement
        #        Permissions via assignment
        rights = { }
        for entity in objects:
            rights[entity] = set()
            rights[entity].add('r')
            rights[entity].add('w')
        return rights


class NoteAccessManager(EntityAccessManager):
    #TODO: Implement!
    __entity__ = 'Note'

    def __init__(self, ctx):
        EntityAccessManager.__init__(self, ctx)

    def implied_rights(self, objects):
        # TODO: Implement
        #        Permissions via assignment
        rights = { }
        for entity in objects:
            rights[entity] = set()
            rights[entity].add('r')
            rights[entity].add('w')
        return rights
        