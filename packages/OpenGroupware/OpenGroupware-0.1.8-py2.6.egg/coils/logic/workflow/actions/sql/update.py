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
import os
from lxml                import etree
from coils.core          import *
from coils.core.logic    import ActionCommand
from utility             import sql_connect

class UpdateAction(ActionCommand):
    __domain__    = "action"
    __operation__ = "sql-update"
    __aliases__   = [ 'sqlUpdate', 'sqlUpdateAction' ]

    def __init__(self):
        ActionCommand.__init__(self)

    def do_action(self):
        db = sql_connect(self._source)
        cursor = db.cursor()
        source = etree.parse(self._rfile)
        table = source.getroot().attrib.get('tableName')
        for row in source.xpath('/ResultSet/row'):
            fields = {}
            keys   = {}
            for field in row.iterchildren():
                name  = field.tag.lower()
                # Determine if value is primary key
                is_key    = field.attrib.get('isPrimaryKey', 'false').lower()
                is_null   = field.attrib.get('isNull', 'false').lower()
                if (name in self._keys):
                    is_key = 'true'
                # Process field value
                if (is_null == 'true'):
                    value = None
                else:
                    # Get field value
                    data_type = field.attrib.get('dataType', None)
                    if ((data_type is None) or (data_type == 'string')):
                        value = self.decode_text(field.text)
                    elif (data_type == 'float'):
                        value = float(field.text)
                    elif (data_type == 'integer'):
                        value = int(field.text)
                # Set as key or value
                if (is_key == 'true'):
                    keys[name] = value
                else:
                    fields[name] = value
            if (len(fields) == 0):
                continue
            if (len(keys) == 0):
                raise CoilsException('No primary keys provided for update of SQL record.')

            values = []

            set_string = ''
            for i in range(0,len(fields)):
                if (i > 0):
                    set_string = set_string + ', '
                set_string = set_string + '{0} = :{1}'.format(fields.keys()[i], i + 1)
                values.append(fields.values()[i])

            key_string = ''
            for i in range(0,len(keys)):
                if (i > 0):
                    key_string = key_string + ' AND '
                key_string = key_string + '{0} = :{1}'.format(keys.keys()[i], i + len(fields) + 1)
                values.append(keys.values()[i])

            sql = 'UPDATE {0} SET {1} WHERE ({2})'.format(table, set_string, key_string)
            self.log.debug(sql)
            self.log.debug(values)
            cursor.execute(sql, values)
            values = fields = keys = set_string = key_string = sql = None
        cursor.close()
        db.close()

    def parse_action_parameters(self):
        self._source = self._params.get('dataSource', None)
        self._keys   = self._params.get('primaryKeys', '').split(',')
        if (self._source is None):
            raise CoilsException('No source defined for selectAction')

    def do_epilogue(self):
        pass