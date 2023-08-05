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
import StringIO, csv
from coils.core           import CoilsException
from format               import COILS_FORMAT_DESCRIPTION_OK
from line_oriented_format import LineOrientedFormat
from exception            import RecordFormatException

class SimpleDelimitedFieldFormat(LineOrientedFormat):

    def __init__(self):
        LineOrientedFormat.__init__(self)

    def set_description(self, fd):
        code = LineOrientedFormat.set_description(self, fd)
        if (code[0] == 0):
            # TODO: Read quoting and delimiter from format definition
            #self.log.error('Value of skipLeadingLines is {0}'.format(self._skip_lines))
            return (COILS_FORMAT_DESCRIPTION_OK, 'OK')
        else:
            return code

    @property
    def mimetype(self):
        return 'text/plain'

    def process_in(self, rfile, wfile):
        # TODO: Read quoting and delimiter from format definition
        self._input = rfile
        self._result = []
        wfile.write(u'<?xml version="1.0" encoding="UTF-8"?>')
        wfile.write(u'<ResultSet formatName=\"{0}\" className=\"{1}\" tableName="{2}">'.\
            format(self.description.get('name'),
                   self.__class__.__name__,
                   self.description.get('tableName', '_undefined_')))
        for record in csv.reader(rfile):
            try:
                data = self.process_record_in(record)
            except RecordFormatException, e:
                self.log.warn('Record format exception on record {0}: {1}'.format(self.in_counter, unicode(record)))
                if (self._discard_on_error):
                    self.log.info('Record {0} of input message dropped due to format error'.format(self.in_counter))
                else:
                    raise e
            else:
                if (data is not None):
                    wfile.write(data)
        wfile.write(u'</ResultSet>')
        return

    def process_record_in(self, record):
        row = []
        self.in_counter = self.in_counter + 1
        #self.log.error('Record count {0}'.format(self.in_counter))
        if (self.in_counter <= self._skip_lines):
            self.log.debug('skipped initial line {0}'.format(self.in_counter))
            return None
        if ((record[0:1] == '#') and (self._skip_comment)):
            self.log.debug('skipped commented line{0}'.format(self.in_counter))
            return None
        if ((len(record) == 0) and (self._skip_blanks)):
            self.log.debug('skipped blank line {0}'.format(self.in_counter))
            return None
        if (len(record) < len(self._definition.get('fields'))):
            raise RecordFormatException('Input record {0} has {1} fields, definition has {2} fields.'.\
                                         format(self.in_counter, len(record), len(self._definition.get('fields'))))
        #self.log.debug('record: {0}'.format(str(record)))
        for i in range(0, len(self._definition.get('fields'))):
            field = self._definition.get('fields')[i]
            value = record[i]
            isKey = str(field.get('key', 'false')).lower()
            try:
                isNull = False
                if (field.get('strip', True)):
                    value = value.strip()
                if (field.get('upper', True)):
                    value = value.upper()
                if (field['kind'] in ['integer', 'float', 'ifloat']):
                    divisor = field.get('divisor', 1)
                    if (field.get('sign', '') == 'a'):
                        sign  = value[-1:] # Take last character as sign
                        value = value[:-1] # Drop last character
                    elif (field.get('sign', '') == 'b'):
                        sign = value[0:1] # Take first character as sign
                        value = value[1:] # Drop first character
                    else:
                        sign = '+'
                    #self.log.debug('sign character for field {0} is {1}'.format(field['name'], sign))
                    if (sign == '+'):
                        sign = 1
                    else:
                        sign = -1
                    if (len(value) == 0):
                        value = field.get('default', None)
                        if (value is None):
                            isNull = True
                    elif (field['kind'] == 'integer'):
                        value = (int(float(value)) * int(sign))
                        if (divisor != 1):
                            value = value / int(divisor)
                    else:
                        value = (float(value) * float(sign))
                        if (divisor != 1):
                            value = value / float(field['divisor'])
                else:
                    value = self.encode_text(value)
            except ValueError, e:
                message = 'Value error converting value \"{0}\" to type \"{1}\" for attribute \"{2}\".'.\
                            format(value, field['kind'], field['name'])
                self.log.warn(message)
                raise RecordFormatException(message, e)
            if (isNull):
                row.append(u'<{0} dataType=\"{1}\" isNull=\"true\" isPrimaryKey=\"{2}\"/>'.\
                    format(field['name'], field['kind'], isKey))
            else:
                row.append(u'<{0} dataType=\"{1}\" isNull=\"false\" isPrimaryKey=\"{2}\">{3}</{4}>'.\
                    format(field['name'], field['kind'], isKey,  value, field['name']))
        return u'<row>{0}</row>'.format(u''.join(row))

    def process_record_out(self, record):
        #TODO: Implement
        raise NotImplementedException()
