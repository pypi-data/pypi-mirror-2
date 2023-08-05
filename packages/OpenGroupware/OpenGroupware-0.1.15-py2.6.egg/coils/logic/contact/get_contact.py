#
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
#
from sqlalchemy          import *
from coils.core          import *
from coils.foundation    import *
from coils.logic.address import GetCompany

class GetContact(GetCompany):
    __domain__ = "contact"
    __operation__ = "get"
    mode = None

    def __init__(self):
        self.access_check = True
        GetCompany.__init__(self)

    def parse_parameters(self, **params):
        GetCompany.parse_parameters(self, **params)
        self._email = None
        if ('email' in params):
            self._email = params.get('email').lower()
            self.mode = 2
        self._archived = params.get('archived', False)

    def run(self):
        db = self._ctx.db_session()
        if (self._email is None):
            if (self._archived):
                query = db.query(Contact).\
                    filter(and_(Contact.object_id.in_(self.object_ids),
                                 Contact.is_person == 1))
            else:
                query = db.query(Contact).\
                    filter(and_(Contact.object_id.in_(self.object_ids),
                                 Contact.is_person == 1,
                                 Contact.status != 'archived'))
        else:
            if (self._archived):
                query = db.query(Contact).join(CompanyValue).\
                    filter(and_(CompanyValue.string_value == self._email,
                                 CompanyValue.name.in_(['email1', 'email2', 'email3'])))
            else:
                query = db.query(Contact).join(CompanyValue).\
                    filter(and_(CompanyValue.string_value == self._email,
                                 CompanyValue.name.in_(['email1', 'email2', 'email3']),
                                 Contact.status != 'archived'))
        self.set_return_value(self.add_comments(query.all()))
