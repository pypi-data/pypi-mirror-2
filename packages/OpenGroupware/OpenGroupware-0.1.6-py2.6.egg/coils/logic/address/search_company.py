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
from datetime         import datetime, timedelta
from pytz             import timezone
from sqlalchemy       import *
from sqlalchemy.orm   import *
from coils.foundation import *
from coils.core       import *
from coils.core.logic import SearchCommand

class SearchCompany(SearchCommand):
    mode = None

    def __init__(self):
        SearchCommand.__init__(self)

    def prepare(self, ctx, **params):
        self._cv = []
        SearchCommand.prepare(self, ctx, **params)

    def _join_company_values(self, query):
        # TODO: Can this be cleaner?
        # Company Values
        if (len(self._cv) > 0):
            cvs = { }
            # Consolidate
            for cv in self._cv:
                key = cv['key'].lower()
                if (cv.has_key('conjunction')):
                    con = cv['conjunction'].lower()
                else:
                    con = 'and'
                if (cv.has_key('expression')):
                    exp = cv['expression'].lower()
                else:
                    exp = 'equals'
                if (not(cvs.has_key(key))):
                    cvs[key] = { 'or': [], 'and': [] }
                if (cv.has_key('value')):
                    v = cv['value']
                else:
                    v = None
                cvs[key][con].append([exp, v])
            # Build joins
            for key in cvs.keys():
                clause = and_()
                t = aliased(CompanyValue)
                # OR
                if (len(cvs[key]['or']) > 0):
                    or_clause = or_()
                    for q in cvs[key]['or']:
                        exp = q[0]
                        v   = q[1]
                        if (exp == 'equals'):
                            or_clause.append(t.string_value==v)
                        elif (exp == 'ilike'):
                            or_clause.append(t.string_value.ilike(v))
                        elif (exp == 'like'):
                            or_clause.append(t.string_value.like(v))
                    clause.append(or_clause)
                # AND
                for q in cvs[key]['and']:
                    exp = q[0]
                    v   = q[1]
                    if (exp == 'equals'):
                        clause.append(t.string_value==v)
                    elif (exp == 'ilike'):
                        clause.append(t.string_value.ilike(v))
                    elif (exp == 'like'):
                        clause.append(t.string_value.like(v))
                # JOIN
                x = and_()
                x.append(t.name==key)
                x.append(clause)
                query = query.join(t).filter(x)
        return query

    def _parse_criteria(self, criteria, entity, keymap):
        query = self._get_query()
        _or = or_()
        _and = and_()
        for criterion in criteria:
            (k,v) = self._translate_criterion(criterion, entity, keymap)
            #print 'Key: %s Value: %s' % (k, v)
            if (k is not None):
                # select conjunction
                if (criterion.has_key('conjunction') and criterion['conjunction'] == 'OR'):
                    conjunction = _or
                else:
                    conjunction = _and
                # expression
                if (criterion.has_key('expression') and (criterion['expression'] == 'ILIKE')):
                    # TODO: replace * characters with %
                    conjunction.append(k.ilike(v))
                elif (criterion.has_key('expression') and (criterion['expression'] == 'LIKE')):
                    # TODO: replace * characters with %
                    conjunction.append(k.like(v))
                else:
                    conjunction.append(k==v)
        query = self._join_company_values(query)
        query = self._join_object_properties(query)
        # Assembly query
        if (len(_or) > 0):
            # put the or in the and
            _and.append(_or)
        if (len(_and) > 0):
            query = query.filter(_and)
        # Log query
        self.log.debug('SQL: {0}'.format(query.statement))
        return query