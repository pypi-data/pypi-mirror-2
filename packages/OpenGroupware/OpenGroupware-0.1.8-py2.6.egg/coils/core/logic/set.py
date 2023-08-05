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
from datetime         import datetime, timedelta
from pytz             import timezone
from sqlalchemy       import *
from coils.foundation import *
from coils.core       import *

class SetCommand(Command):

    def __init__(self):
        self.values = None
        Command.__init__(self)

    def _sync_entities(self, source, target):
        insert = []
        update = []
        remove = {}
        for entity in target:
            remove[entity.object_id] = entity
        for s in source:
            for t in target:
                if (isinstance(s, dict)):
                    if (t.object_id == s.get('object_id', 0)):
                        update.append({'entity': t, 'values': s})
                        del remove[t.object_id]
                        break
                elif (hasattr(s, 'object_id')):
                    if (t.object_id == s.object_id):
                        update.append({'entity': t, 'values': s})
                        del remove[t.object_id]
                        break
            else:
                insert.append(s)
        return (insert, update, remove.values())

    def save_acls(self):
        if (hasattr(self.obj, 'acls')):
            target = getattr(self.obj, 'acls')
            source = KVC.subvalues_for_key(self.values, ['_ACLS', 'acls'])

    def save_notes(self):
        if (hasattr(self.obj, 'notes')):
            target = getattr(self.obj, 'notes')
            source = KVC.subvalues_for_key(self.values, ['_NOTES', 'notes'])
            (insert, update, delete) = self._sync_entities(source, target)
            for value in insert:
                self._ctx.run_command('note::new', values=value, context=self.obj)
            for value in update:
                self._ctx.run_command('note::set', values=value.get('values'),
                                                   entity=value.get('entity'),
                                                   context=self.obj)
            for value in delete:
                self._ctx.run_command('note::delete', object=value)

    def save_properties(self):
        if (hasattr(self.obj, 'properties')):
            properties = KVC.subvalues_for_key(self.values, ['_PROPERTIES', 'properties'], None)
            if (properties is not None):
                self._ctx.property_manager.set_properties(self.obj, properties)

    def save_subordinates(self):
        self.save_acls()
        self.save_notes()
        self.save_properties()

    def epilogue(self):
        Command.epilogue(self)
        Command.notify(self)
