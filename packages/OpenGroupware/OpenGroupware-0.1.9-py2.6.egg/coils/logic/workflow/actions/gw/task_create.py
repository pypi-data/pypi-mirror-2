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
from pytz                import timezone
from datetime            import datetime, timedelta
from coils.core          import *
from coils.core.logic    import ActionCommand
from coils.core.xml      import Render as XML_Render

class CreateTaskAction(ActionCommand):
    __domain__ = "action"
    __operation__ = "create-task"
    __aliases__   = [ 'createTask', "createTaskAction" ]

    def __init__(self):
        ActionCommand.__init__(self)

    def do_action(self):
        task = self._ctx.run_command('task::new', values=values)
        if (task is None):
            raise CoilsException('Failed to create entity.')
        if (self._tiein):
            self._process.task_id = task.object_id
        results = XML_Render.render(task, self._ctx)
        self._wfile.write(results)
        self._wfile.flush()

    def parse_action_parameters(self):
        self._values = {
            'comment':     self.process_label_substitutions(self._params.get('comment', '')),
            'name':        self.process_label_substitutions(self._params.get('name', '')),
            'start':       self.process_label_substitutions(self._params.get('start', '')),
            'end':         self.process_label_substitutions(self._params.get('end', '')),
            'parentid':    int(self.process_label_substitutions(str(self._params.get('parent', None)))),
            'ownerid':     self.process_label_substitutions(self._params.get('owner', str(self._ctx.account_id))),
            'kind':        self.process_label_substitutions(self._params.get('kind', '')),
            'sensitivity': int(self.process_label_substitutions(str(self._params.get('sensitivity', '0')))),
            'priority':    self.process_label_substitutions(self._params.get('priority', '3')),
            'executorid':  int(self.process_label_substitutions(str(self._params.get('executor', self._ctx.account_id))))
            }
        if ('duration' in self._params):
            self._values['start'] += timedelta(days=int(self._params.get('duration')))
        if (len(self._values['kind']) == 0): self._values['kind'] = None
        if (len(self._values['parentid']) == 0): self._values['parentid'] = None
        if (len(self._values['start']) == 0): self._values['start'] = None
        if (len(self._values['end']) == 0): self._values['end'] = None
        if (self._params('workflowTask', 'YES').upper() == 'YES'):
            self._tiein = True
        else:
            self._tiein = False

    def do_epilogue(self):
        size = os.path.getsize(self._filename)
        self.log_message('readAction: Created {0} octets of output'.format(size))
