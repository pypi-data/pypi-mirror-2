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
import sys
import xmldict, urllib
from StringIO import StringIO
from coils.core import *
from coils.net import *
from bufferedwriter import BufferedWriter
from reports import Parser
from xml.sax.saxutils    import escape
from useragent import UserAgent

PATH_CACHE = { }
USE_CACHE = False

PROP_METHOD    = 0
PROP_NAMESPACE = 1
PROP_LOCALNAME = 2
PROP_DOMAIN    = 3

class DAV(PathObject):
    def __init__(self, parent, name, **params):
        ''' Root DAV Object;  provides utility methods for implementing WebDAV.

        Keyword Arguments:
        parent - The parent object in the DAV hierarchy, should be a DAV object
        name - The name of this object, as used in the URL

        Additional named parameters are used to directly set attributes of this
        object,  so you you set fred=123 an attribute of fred will be set on the
        object with a value of 123.
        '''
        self.name = name
        self.data = None
        PathObject.__init__(self, parent, **params)

    @property
    def user_agent(self):
        return UserAgent(self.request.headers.get('USER-AGENT', None))

    def get_path(self):
        ''' Reconstruct the path used to arrive at this object'''
        path = self.name
        x = self.parent
        while (x is not None):
            path = '%s/%s' % (x.get_name(), path)
            x = x.parent
        return path

    @property
    def url(self):
        return self.get_path()[1:]

    #
    # Properties
    #

    def get_ctag(self):
        ''' Return a ctag appropriate for this object.
            Actual WebDAV objects should override this method '''
        # Child should override, it knows how to compute or derive its ctag.
        return '0'

    # PROP: EXECUTABLE

    def get_property_unknown_executable(self):
        return self.get_property_webdav_executable()

    def get_property_webdav_executable(self):
        return '0'

    #
    # Data & Cache
    #

    def get_cached_value(self, key):
        if(USE_CACHE):
            path = '%d:%s' % (self.context.account_id, self.get_path())
            v = None
            if (PATH_CACHE.has_key(path)):
                ctag = self.get_ctag()
                if (PATH_CACHE[path]['ctag'] == ctag):
                    if (PATH_CACHE[path]['data'].has_key(key)):
                        # Path cached and current, key found
                        v = PATH_CACHE[path]['data'][key]
                    else:
                        # Path cached and current, but no such key
                        v = None
                else:
                    # Path cached but not current: wipe cache
                    PATH_CACHE[path] = { 'ctag': ctag, 'data': { } }
                    v = None
            return v
        else:
            return None

    def put_value_to_cache(self, key, value):
        if (USE_CACHE):
            path = '%d:%s' % (self.context.account_id, self.get_path())
            ctag = self.get_ctag()
            if ((not(PATH_CACHE.has_key(path))) or
                (PATH_CACHE[path]['ctag'] != ctag)):
                PATH_CACHE[path] = { 'ctag': ctag, 'data': { } }
            PATH_CACHE[path]['data'][key] = value

    def load_self(self):
        ''' If the DAV objects does not contain any data (self.data is None) then
            an attempt is made to retrieve the relevent information.  This method
            calls the _load_self() which the child is expected to implement. '''
        if (self.data is None):
            x = self.get_cached_value('contents')
            if (x is not None):
                self.data = x
                return True
            if (self._load_self()):
                self.put_value_to_cache('contents', self.data)
                return True
            return False
        return True

    #
    # OPTIONS supports
    #

    def supports_GET(self):
        return False

    def supports_POST(self):
        return False

    def supports_PUT(self):
        return False

    def supports_DELETE(self):
        return False

    def supports_PROPFIND(self):
        return True

    def supports_PROPATCH(self):
        return False

    def supports_MKCOL(self):
        return False

    def get_methods(self):
        return ['GET', 'POST', 'PUT', 'DELETE', 'PROPFIND', 'PROPPATCH', 'MKCOL']

    def supports_operation(self, operation):
        operation = operation.upper().strip()
        method = 'supports_{0}'.format(operation)
        if (hasattr(self, method)):
            return getattr(self, method)()
        return False

    def do_OPTIONS(self):
        ''' Return a valid WebDAV OPTIONS response '''
        self.request.send_response(200, 'OpenGroupware.org COILS')
        methods = [ 'HEAD', 'OPTIONS' ]
        for method in self.get_methods():
            if (self.supports_operation(method)):
                methods.append(method)
        self.request.send_header('Allow', ','.join(methods))
        methods = None
        self.request.send_header('Content-length', '0')
        self.request.send_header('DAV', '1')
        self.request.send_header('MS-Author-Via', 'DAV')
        self.request.end_headers()

    #
    # Properties support
    #

    def parse_propfind_for_property_names(self, payload):
        return Parser.propfind(payload)

    def self_propfind(self, path, props, w):
        # Multistatus provides a response for each resource
        # a response contains an href and a propstat
        self.log.debug('self (depth=0) propfind on {0}'.format(self))
        unknown = [ ]
        known  = { }
        w.write(u'<?xml version="1.0" encoding="utf-8"?>')
        w.write(u'<D:multistatus xmlns:D="DAV:">')
        if (hasattr(self, 'location') and self.user_agent.supports_301):
            self.propfind_response(props, self.location, self, w)
        else:
            self.propfind_response(props, self.get_path()[1:], self, w)
        w.write(u'</D:multistatus>')

    def propfind_response(self, props, key, resource, w):
        #
        # TODO: What is the correct thing to do for a moved resource?
        #        Reply with the href requested or reply with the
        #        resources "real" location?
        #
        known = {}
        unknown = []
        w.write(u'<D:response>')
        #w.write(u'<D:href>{0}</D:href>'.format(escape(key)))
        w.write(u'<D:href>{0}</D:href>'.format(urllib.quote(resource.url)))
        for i in range(len(props)):
            prop = props[i]
            if (hasattr(resource, prop[PROP_METHOD])):
                x = getattr(resource, prop[PROP_METHOD])
                value = str(x())
                x = None
                if (value[0:1] != u'<'):
                    known[prop] = escape(value)
                else:
                    known[prop] = value
            else:
                self.log.debug('No such method as {0} on {1}.'.format(prop[PROP_METHOD], resource))
                unknown.append(prop)
        # render found properties
        if (len(known) > 0):
            w.write(u'<D:propstat>')
            w.write(u'<D:status>HTTP/1.1 200 OK</D:status>')
            for prop in known.keys():
                w.write(u'<D:prop>')
                if (known[prop] is None):
                    # PROPERTY VALUE NONE
                    if (prop[PROP_DOMAIN] == u'webdav'):
                        w.write(u'<D:%s/>' % prop[PROP_LOCALNAME])
                    elif (prop[PROP_NAMESPACE] is None):
                        w.write(u'<{0}/>'.format(prop[PROP_LOCALNAME]))
                    else:
                        w.write(u'<{0} xmlns="{1}"/>'.format(prop[PROP_LOCALNAME],
                                                             prop[PROP_NAMESPACE]))
                else:
                   # PROPERTY HAS VALUE
                    if (prop[PROP_DOMAIN] == u'webdav'):
                        w.write(u'<D:{0}>{1}</D:{2}>'.format(prop[PROP_LOCALNAME],
                                                             known[prop],
                                                             prop[PROP_LOCALNAME]))
                    elif (prop[PROP_NAMESPACE] is None):
                        w.write(u'<{0}>{1}</{2}>'.format(prop[PROP_LOCALNAME],
                                                         known[prop],
                                                         prop[PROP_LOCALNAME]))
                    else:
                        w.write(u'<{0} xmlns="{1}">{2}</{3}>'.format(prop[PROP_LOCALNAME],
                                                                     prop[PROP_NAMESPACE],
                                                                     known[prop],
                                                                     prop[PROP_LOCALNAME]))
                w.write(u'</D:prop>')
            w.write(u'</D:propstat>')
        # UNKNOWN PROPERTIES
        if (len(unknown) > 0):
            w.write(u'<D:propstat>')
            w.write(u'<D:status>HTTP/1.1 404 Not found</D:status>')
            for prop in unknown:
                if (prop[PROP_DOMAIN] == 'webdav'):
                    w.write(u'<D:prop><D:{0}/></D:prop>'.format(prop[PROP_LOCALNAME]))
                elif (prop[PROP_NAMESPACE] is None):
                    w.write(u'<D:prop><{0}/></D:prop>'.format(prop[PROP_LOCALNAME]))
                else:
                    w.write(u'<D:prop><{0} xmlns="{1}"/></D:prop>'.format(prop[PROP_LOCALNAME],
                                                                          prop[PROP_NAMESPACE]))
            w.write(u'</D:propstat>')
        w.write(u'</D:response>')
