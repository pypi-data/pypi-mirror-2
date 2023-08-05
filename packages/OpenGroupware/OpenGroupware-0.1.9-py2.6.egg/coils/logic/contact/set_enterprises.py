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
from sqlalchemy       import *
from coils.core       import *
from coils.foundation import diff_id_lists, Contact, Enterprise, CompanyAssignment
from command          import ContactCommand


class SetEnterprises(Command, ContactCommand):
    __domain__      = "contact"
    __operation__   = "set-enterprises"
    mode = None

    def __init__(self):
        Command.__init__(self)

    def parse_parameters(self, **params):
        # appointment_id is *ONLY* used to lookup the appointment, setting
        # self.appointment as if an appointment object was provided - that
        # happens in run().  Appointment id should *NOT* be used, always
        # reference self.appointment.object_id.
        Command.parse_parameters(self, **params)
        self.contact       = params.get('contact', None)
        self.contact_id    = params.get('contact_id', None)
        if ('enterprises' in params):
            self.enterprise_ids = []
            for enterprise in params.get('enterprises'):
                self.enterprise_ids.append(enterprise.object_id)
        elif ('enterprise_ids' in params):
            self.enterprise_ids = params.get('enterprise_ids')

    def check_parameters(self):
        if ((self.contact_id is None) and (self.contact is None)):
            raise CoilsException('No contact provided to set-enterprises')

    def get_contact(self):
        # If contact wasn't provided, use contact_id to look it up.
        if (self.contact is None):
            self.contact = self.get_by_id(self.contact_id, self.access_check)
        if (self.contact is None):
            raise 'Enterprise set cannot identify the relevant contact'
        else:
            # TODO: Check for write access!
            self._result = True

    def run(self):
        db = self._ctx.db_session()
        self.check_parameters()
        self.get_contact()
        # Get list of enterprise ids contact is assigned to
        assigned = []
        for assignment in self.contact.enterprises:
            assigned.append(assignment.parent_id)
        # Perform inserts and updates
        db = self._ctx.db_session()
        # Add new enterprise assignments
        for enterprise_id in self.enterprise_ids:
            if (enterprise_id not in assigned):
                x = CompanyAssignment(enterprise_id, self.contact.object_id)
                db.add(x)
        # Remove expired assignments
        db.query(CompanyAssignment).\
            filter(and_(not_(CompanyAssignment.parent_id.in_(self.enterprise_ids)),
                         CompanyAssignment.child_id == self.contact.object_id)).delete()
