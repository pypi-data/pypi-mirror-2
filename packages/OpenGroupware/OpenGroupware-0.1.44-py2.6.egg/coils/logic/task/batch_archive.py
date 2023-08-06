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
import uuid
from datetime           import timedelta, datetime
from sqlalchemy         import *
from coils.core         import *
from command            import TaskCommand

class BatchArchive(Command, TaskCommand):
    __domain__    = "task"
    __operation__ = "batch-archive"

    def parse_parameters(self, **params):
        Command.parse_parameters(self, **params)
        if ('age' in params):
            self._age = int(params.get('age'))
            self._owner = None
        elif ('owner_id' in params):
            self._owner = int(params.get('owner_id'))
        else:
            raise CoilsException('Neither owner nor age specified for batch archive.')

    def run(self):
        if (self._ctx.is_admin):
            counter = 0
            db = self._ctx.db_session()
            comment = 'Auto-archived by administrative event {{{0}}}'.format(str(uuid.uuid4()))
            if (self._owner is None):
                # Assuming Age (archive old tasks) mode
                now = datetime.now()
                span = timedelta(days=self._age)
                query = db.query(Task).filter(and_(Task.state.in_('25_done', '02_rejected'),
                                                   Task.completed is not None,
                                                   Task.completed < (now - span) ) )
            else:
                # Assuming archive tasks for specified owner mode
                query = db.query(Task).filter(and_(Task.owner_id == self._owner,
                                                   Task.state.in_('25_done', '02_rejected')))
            for task in query.all():
                self._ctx.run_command('task::comment', task=task,
                                                       values={ 'comment': comment,
                                                                'action': 'archive'        } )
                counter += 1
                # TODO: Perform notification of event
            self._result = counter
        else:
            raise CoilsException('Insufficient privilages to execute task::batch-archive')
