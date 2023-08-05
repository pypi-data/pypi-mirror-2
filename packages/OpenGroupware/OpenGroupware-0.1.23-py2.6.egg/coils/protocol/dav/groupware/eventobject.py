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
# THE SOFTWARE.
#
import io
from datetime                          import datetime
# Core
#from coils.core                        import *
#from coils.net                         import *
# DAV Classses
from coils.protocol.dav.foundation     import DAVObject

class EventObject(DAVObject):

    def __init__(self, parent, name, **params):
        DAVObject.__init__(self, parent, name, **params)

    def get_property_webdav_displayname(self):
        if (self.entity.title is None):
            return 'Appointment Id#{0}'.format(self.entity.object_id)
        else:
            return self.entity.title

    def get_property_webdav_name(self):
        return str(self.entity.object_id)

    # PROP: GETETAG

    def get_property_unknown_getetag(self):
        return self.get_property_webdav_getetag()

    def get_property_cadaver_getetag(self):
        return self.get_property_webdav_getetag()

    def get_property_caldav_getetag(self):
        return self.get_property_webdav_getetag()

    def get_property_webdav_getetag(self):
        return '{0}:{1}'.format(self.entity.object_id, self.entity.version)

    # PROP: GETCONTENTLENGTH

    def get_property_webdav_getcontentlength(self):
        return str(len(self.get_representation()))

    def get_property_webdav_getcontenttype(self):
        return 'text/calendar'

    def get_property_caldav_calendar_data(self):
        return self.get_representation()

    #def get_property_CREATIONDATE(self):
    #    if (self.entity.created is None):
    #        return datetime.now()
    #    else:
    #        return self.entity.created

    def do_DELETE(self):
        if_etag = self.request.headers.get('If-Match', None)
        if (if_etag is None):
            self.log.warn('Client issued a deletion operation with no If-Match!')
        else:
            if_etag = if_etag.replace('"', '')
            is_etag = self.get_property_webdav_getetag()
            if (if_etag != is_etag):
                self.request,send_response(412, 'Pre-condition failed')
                self.request.end_headers()
                return
        try:
            self.context.run_command('appointment::delete', object=self.entity)
            self.entity = None
            self.context.commit()
        except Exception, e:
            self.log.exception(e)
            self.log.warn('Failure to delete appointment id#{0}'.format(self.entity.object_id))
        else:
            self.request.send_response(204, 'No Content')
            self.request.end_headers()