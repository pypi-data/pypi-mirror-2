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
from time import strftime, gmtime, time
# Core
from coils.foundation   import *
from coils.core         import *
from coils.net          import *
# DAV Classses
from bufferedwriter     import BufferedWriter
from dav                import DAV
from reports            import Parser

from entity_map         import ENTITYMAP

class DAVObject(DAV):
    """ Represents an OpenGroupware entity in a DAV collection,  a GET will return the
        representation of the object - vCard, vEvent, vToDo, etc... """

    # The self.data in a DAVObject  to be a first-class ORM entity
    def __init__(self, parent, name, **params):
        #self.location = None
        DAV.__init__(self, parent, name, **params)
        self._representation = None

    #
    # Core
    #

    @property
    def is_object(self):
        return True

    #
    # Properties
    #

    def supports_GET(self):
        return True

    def get_property_getetag(self):
        if (self.load_contents()):
            if (hasattr(self.entity, 'object_id')):
                left = str(self.entity.object_id)
            elif (hasattr(self.entity, 'uuid')):
                left = self.entity.uuid.strip()
            else:
                raise CoilsException('No candidate property for etag creation')
        if (hasattr(self.entity, 'version')):
            return '{0}:{1}'.format(left, self.entity.version)
        else:
            return '{0}:0'.format(left)

    def get_property_unknown_getetag(self):
        return self.get_property_getetag()

    def get_property_webdav_getetag(self):
        return self.get_property_getetag()

    # PROP: ISCOLLECTION

    def get_property_unknown_iscollection(self):
        return self.get_property_webdav_iscollection()

    def get_property_webdav_iscollection(self):
        return '0'

    # PROP: DISPLAYNAME

    def get_property_unknown_displayname(self):
        return self.get_property_webdav_displayname()

    def get_property_webdav_displayname(self):
        return self.name

    # PROP: RESOURCETYPE

    def get_property_unknown_resourcetype(self):
        return self.get_property_webdav_resourcetype(self)

    def get_property_webdav_resourcetype(self):
        return ''

    # PROP: GETCONTENTLENGTH

    def get_property_unknown_getcontentlength(self):
        return self.get_property_webdav_getcontentlength()

    def get_property_webdav_getcontentlength(self):
        #if (self._get_representation()):
        #    return str(len(self.data))
        return '0'

    # PROP: GETCONTENTTYPE

    def get_property_unknown_getcontenttype(self):
        return get_property_webdav_getcontenttype(self)

    def get_property_webdav_getcontenttype(self):
        if (hasattr(self.entity, '__entityName__')):
            if self.entity.__entityName__ in ENTITYMAP:
                return ENTITYMAP[self.entity.__entityName__]['mime-type']
        return 'application/octet-stream'

    # PROP: HREF

    def get_property_unknown_href(self):
        return self.get_property_webdav_href()

    def get_property_webdav_href(self):
        if (hasattr(self, 'location')):
            return self.location
        return self.webdav_url

    # PROP: CREATIONDATE

    def get_property_unknown_creationdate(self):
        return self.get_property_webdav_creationdate()

    def get_property_webdav_creationdate(self):
        x = gmtime(time())
        return strftime("%a, %d %b %Y %H:%M:%S GMT", x)


    # PROP: GETLASTMODIFIED

    def get_property_unknown_getlastmodified(self):
        return self.get_property_webdav_getlastmodified()

    def get_property_webdav_getlastmodified(self):
        #TODO: This format is not correct - no timezone
        if ((self.load_contents()) and hasattr(self.entity, 'modified')):
            x = self.entity.modified
        else:
            x = gmtime(time())
        return strftime("%a, %d %b %Y %H:%M:%S GMT", x)

    # DATA LOAD
    def get_keys(self):
        return None

    def _load_contents(self):
        if (self.entity is None):
            if (self.name.isdigit()):
                object_id = int(self.name)
                kind = self.context.type_manager.get_type(object_id)
                if (kind == 'Unknown'):
                    return False
                self.entity = self.context.run_command(ENTITYMAP[kind]['get-command'], id=object_id)
                if (self.entity is None):
                    return False
            else:
                return False
        return True

    def get_representation(self):
        x = self.get_cached_value('representation')
        if (x is None):
            if (self.load_contents()):
                command = ENTITYMAP[self.entity.__entityName__]['data-command']
                self.log.debug('Selected {0} to retrieve object representation.'.format(command))
                x = self.context.run_command(ENTITYMAP[self.entity.__entityName__]['data-command'],
                                             object=self.entity)
                if (x is None):
                    self.log.warn('Data command for object representation returned None!')
                    return ''
        self.put_value_to_cache('representation', x)
        return x

    def do_GET(self):
        if (hasattr(self, 'location') and self.location is not None):
            if (self.user_agent.supports_301):
                self.request.send_response(301, 'Moved')
                self.request.send_header('Location', self.location)
                self.request.end_headers()
                return
            self.log.warn('Request from DAV client known to not support 301 responses.')
        payload = self.get_representation()
        if (payload is not None):
            w = BufferedWriter(self.request.wfile, False)
            w.write(payload)
            self.request.send_response(200, 'OK')
            self.request.send_header('Content-Length', str(w.getSize()))
            self.request.send_header('etag', self.get_property_getetag())
            self.request.send_header('Content-Type', ENTITYMAP[self.entity.__entityName__]['mime-type'])
            self.request.end_headers()
            w.flush()
            w = None
            return
        else:
            raise NoSuchPathException('%s not found' % self.name)

    def do_HEAD(self):
        if (hasattr(self, 'location')):
            self.request.send_response(301, 'Moved')
            self.request.send_header('Location', self.location)
            self.request.end_headers()
        else:
            x = self.get_representation()
            if (x is not None):
                self.request.send_response(200, 'OK')
                self.request.send_header('Content-Length', str(w.getSize()))
                self.request.send_header('etag', self.get_property_getetag())
                self.request.send_header('Content-Type', ENTITYMAP[self.entity.__entityName__]['mime-type'])
                self.request.end_headers()
                return
            else:
                raise NoSuchPathException('%s not found' % self.name)
