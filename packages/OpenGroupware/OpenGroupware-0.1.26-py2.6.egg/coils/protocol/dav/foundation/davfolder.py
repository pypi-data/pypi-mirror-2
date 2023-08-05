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
from coils.foundation       import *
from coils.core             import *
from dav                    import DAV
from bufferedwriter         import BufferedWriter
from reports                import Parser
from davobject              import DAVObject

PROP_METHOD    = 0
PROP_NAMESPACE = 1
PROP_LOCALNAME = 2
PROP_DOMAIN    = 3

class DAVFolder(DAV):
    ''' Represents a DAV collection (folder).

        self.data is expected to be dict, where the key is the DAV name of the
        resource within the collection.  The contents of the value is a *list*
        where the first object is the Entity (Contact, Enterprise, Project,
        etc...) which the child represents.  That entity is passed to the
        new child object as 'entity'. '''

    def __init__(self, parent, name, **params):
        DAV.__init__(self, parent, name, **params)

    #
    # Core
    #

    @property
    def is_folder(self):
        return True

    # PROP: CREATIONDATE

    def get_property_unknown_creationdate(self):
        return self.get_property_webdav_creationdate()

    def get_property_webdav_creationdate(self):
        ''' Returns the value of the 'is collection' property which is always
            a value of '1'.  Believe this to be a non-standard WebDAV
            attribute. '''
        return u'1997-12-01T17:42:21-08:00'

    # PROP: ISCOLLECTION

    def get_property_unknown_iscollection(self):
        return self.get_property_webdav_iscollection()

    def get_property_webdav_iscollection(self):
        ''' Returns the value of the 'is collection' property which is always
            a value of '1'.  Believe this to be a non-standard WebDAV
            attribute. '''
        return '1'

    # PROP: RESOURCETYPE

    def get_property_unknown_resourcetype(self):
        return self.get_property_webdav_resourcetype(self)

    def get_property_webdav_resourcetype(self):
        ''' Return the resource type of the collection, which is always
            'collection'.

            See RFC2518, Section 13.9'''

        return u'<collection/>'

    # PROP: GETCONTENTTYPE

    def get_property_unknown_getcontenttype(self):
        return self.get_property_webdav_getcontenttype(self)

    def get_property_webdav_getcontenttype(self):
        ''' Return the resource type of the collection, which is always
            'collection'.

            See RFC2518, Section 13.9'''

        return u'unix/httpd-directory'

    # PROP: GETLASTMODIFIED

    def get_property_unknown_getlastmodified(self):
        return self.get_property_webdav_getlastmodified()

    def get_property_webdav_getlastmodified(self):
        ''' Return the last modified timestamp of this collection.  It is
            impossible for our data-model to support this property so we
            always return the current date and time in GMT.

            See RFC2518, Section 13.7 '''

        return strftime("%a, %d %b %Y %H:%M:%S", gmtime(time()))

    # PROP: GETCONTENTLENGTH

    def get_property_unknown_getcontentlength(self):
        return self.get_property_webdav_getcontentlength()

    def get_property_webdav_getcontentlength(self):
        ''' Retun the content-length of the collection. The content length of
            a collection is always 0.

            See RFC2518, Section 13.4 '''
        return u'0'

    # PROP: DISPLAYNAME

    def get_property_unknown_displayname(self):
        return self.get_property_webdav_displayname()

    def get_property_webdav_displayname(self):
        ''' Return the displayName of the collection.

            Used by PROPFIND requests.'''
        return self.name

    # PROP: HREF

    def get_property_unknown_href(self):
        return self.get_property_webdav_href()

    def get_property_webdav_href(self):
        if (hasattr(self, 'location')):
            return self.location
        return self.get_path()

    # Name

    def get_name(self):
        ''' Return the name of the collection, this is the name in the URL
            which the client requested.'''
        return self.name

    def do_HEAD(self):
        self.request.send_response(201, 'OK')
        #TODO: Put WebDAV folder headers here
        self.request.end_headers()

    def no_such_path(self):
        raise NoSuchPathException('Not such path as {0}'.format(self.request.path))

    def object_for_key(self, name, auto_load_enabled=True, is_webdav=False):
        '''Retrieve the DAV object for the specified name.'''
        if (auto_load_enabled): self.load_contents()
        if (self.is_loaded):
            x = self.get_child(name)
            if (x is not None):
                return x
        # Send a 404 (No found) error
        self.no_such_path()

    def get_object_for_key(self, name, auto_load_enabled=True, is_webdav=False):
        return self.object_for_key(name, auto_load_enabled=auto_load_enabled, is_webdav=is_webdav)

    def do_GET(self):
       w = BufferedWriter(self.request.wfile, False)
       w.write('GET requests are not supported on collection objects, use a WebDAV client.\n')
       w.write('Current path {0} is a collection.\n'.format(self.webdav_url))
       self.request.send_response(200, 'OK')
       self.request.send_header('Content-Length', str(w.getSize()))
       self.request.send_header('Content-Type', 'text/plain')
       self.request.end_headers()
       w.flush()
