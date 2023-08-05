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
from coils.core       import *  # Required?
from get              import GetCommand, \
                              RETRIEVAL_MODE_SINGLE, \
                              RETRIEVAL_MODE_MULTIPLE
from keymap      import COILS_ADDRESS_KEYMAP, COILS_TELEPHONE_KEYMAP

class SearchCommand(Command):

    def __init__(self):
        Command.__init__(self)
        self.mode = RETRIEVAL_MODE_MULTIPLE

    def prepare(self, ctx, **params):
        self._result = [ ]
        self._pr     = [ ]
        Command.prepare(self, ctx, **params)

    """
        Keymap Example:     'private':              ['is_private', 'int'],
                            'bossname':             ['boss_name'],
                            'managersname':         ['boss_name'],
                            'managers_name':        ['boss_name'],
                            'sex':                  ['gender'],
                            'deathdate':            ['grave_date', 'date', None],
        This translates the named key into the first value of the corresponding array.  If the
        array has a second value it is: "int" or "date" and the value is translated into the
        corresponding value type.  If the value is None and the array has a third value (a
        "default" value) then the value is replaced with the third value.  Date formats supported
        are "YYYY-MM-DD" and "YYYY-MM-DD HH:mm" where hours are in 0 - 23 not AM/PM.  All dates
        are interpreted as GMT.
    """
    def _translate_key(self, key, value, keymap):
        key = key.lower()
        if (keymap.has_key(key)):
            x = keymap[key]
            # translate key name
            key = x[0]
            # transform value type
            if (len(x) > 1):
                t = x[1]
                if (t == 'int'):
                    # Make sure value is an integer
                    value = int(value)
                elif (t == 'date'):
                    # Deal with date value
                    if (not (isinstance(value, datetime))):
                        # Translate string to datetime
                        if (isinstance(value, str)):
                            if (len(value) == 10):
                                # YYYY-MM-DD
                                value = datetime(int(value[0:4]), int(value[5:7]), int(value[8:10]))
                            elif (len(value) == 16):
                                # YYYY-MM-DD HH:mm [24 hour, no AM/PM crap]
                                value = datetime(int(value[0:4]), int(value[5:7]), int(value[8:10]),
                                                 int(value[11:13]), int(value[14:16]))
                            else:
                                raise CoilsException('Invalid string format for datetime conversion')
                        elif (isinstance(value, int)):
                            value = dateime.utcfromtimestamp(value)
                    # set timezone to UTC
                    value.replace(tzinfo=timezone('UTC'))
            # default value, for None
            if ((len(x) == 3) and (value is None)):
                value = x[2]
        return (key, value)

    def _translate_criterion(self, criterion, entity, keymap):
        v = criterion.get('value', None)
        k = criterion['key'].split('.')
        if (len(k) == 1):
            k = k[0]
            (k, v) = self._translate_key(k, v, keymap)
            if (hasattr(entity, k)):
                return (getattr(entity, k), v)
            elif (hasattr(entity, 'company_values')):
                # company value
                self._cv.append(criterion)
                return (None, None)
        elif (len(k) == 2):
            # address or telephone
            if (hasattr(entity, 'addresses') and (k[0].lower() in ['address'])):
                # address
                k = k[1]
                (k, v) = self._translate_key(k, v, COILS_ADDRESS_KEYMAP)
                if (hasattr(Address, k)):
                    return (getattr(Address, k), v)
                return (None, None)
            elif (hasattr(entity, 'telephones') and (k[0].lower() in ['phone', 'telephone'])):
                k = k[1]
                (k, v) = self._translate_key(k, v, COILS_TELEPHONE_KEYMAP)
                if (hasattr(Telephone, k)):
                    return (getattr(Telephone, k), v)
                return (None, None)
        elif (len(k) == 3):
            # property (?)
            self._pr.append(criterion)
            return (None, None)
        return (None, None)

    def _join_object_properties(self, query):
        # TODO: Implement,  see _join_company_values in contact::search
        # Object Properties
        if (len(self._pr) > 0):
            query = query.outerjoin(ObjectProperty)
        return query

    def set_return_value(self, data):
        if (isinstance(data, list)):
            if (self.access_check):
                data = self._ctx.access_manager().filter_by_access(self._ctx, 'r', data)
            if (len(data) > 0):
                if (self.mode == RETRIEVAL_MODE_SINGLE):
                    self._result = data[0]
                else:
                    self._result = data
            elif (self.mode == RETRIEVAL_MODE_MULTIPLE):
                self._result = [ ]
            elif (self.mode == RETRIEVAL_MODE_SINGLE):
                self._result = None
            else:
                raise CoilsException('Unknown mode value')
            return
        raise CoilsException('Data for Get result is not a list')
        self._result = None