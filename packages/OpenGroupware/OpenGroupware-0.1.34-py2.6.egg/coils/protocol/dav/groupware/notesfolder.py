# Copyright (c) 2010 Tauno Williams <awilliam@whitemice.org>
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
import urllib
from coils.core                        import NoSuchPathException
from coils.core.icalendar              import Parser as ICS_Parser
from coils.protocol.dav.foundation     import DAVFolder, \
                                                Parser, \
                                                BufferedWriter, \
                                                Multistatus
from noteobject                        import NoteObject

class NotesFolder(DAVFolder):
    def __init__(self, parent, name, **params):
        DAVFolder.__init__(self, parent, name, **params)

    def supports_PUT(self):
        return True

    def _load_contents(self):
        notes = self.context.run_command('project::get-notes', id=self.entity.object_id)
        if (self.user_agent.supports_memos):
            print 'memo support detected'
            for note in notes:
                if (note.caldav_uid is None):
                    print 'memoId#{0} has no alias'.format(note.object_id)
                    self.insert_child(note.object_id, note, alias='{0}.vjl'.format(note.object_id))
                else:
                    print 'memoId#{0} has alias {1}'.format(note.object_id, note.caldav_uid)
                    self.insert_child(note.object_id, note, alias=note.caldav_uid)
        else:
            for note in notes: self.insert_child(note.title, note)
        return True

    def object_for_key(self, name, auto_load_enabled=True, is_webdav=False):
        if  (self.load_contents()):
            if (self.has_child(name)):
                return NoteObject(self, name, entity=self.get_child(name),
                                               request=self.request,
                                               context=self.context)
        self.no_such_path()


    def do_OPTIONS(self):
        ''' Return a valid WebDAV OPTIONS response '''
        self.request.send_response(200, 'OpenGroupware.org COILS')
        #methods = [ 'HEAD', 'OPTIONS' ]
        #for method in self.get_methods():
        #    if (self.supports_operation(method)):
        #        methods.append(method)
        self.request.send_header('Allow', 'OPTIONS, GET, HEAD, POST, PUT, DELETE, TRACE, COPY, MOVE')
        self.request.send_header('Allow', 'PROPFIND, PROPPATCH, LOCK, UNLOCK, REPORT, ACL')
        #self.request.send_header('Allow', ','.join(methods))
        #methods = None
        self.request.send_header('Content-length', '0')
        self.request.send_header('DAV', '1, 2, access-control, calendar-access')
        self.request.send_header('MS-Author-Via', 'DAV')
        self.request.end_headers()

    def do_PUT(self, request_name):
        mimetype = self.request.headers.get('CONTENT-TYPE', 'text/plain').split(';')[0].lower()
        # TODO: Support If-Match header!
        if (self.load_contents()):
            self.log.debug('Requested label is {0}.'.format(request_name))
            payload = self.request.get_request_payload()
            # Process payload and request name
            if (mimetype == 'text/calendar'):
                # CalDAV Mode (memo operations)
                values = ICS_Parser.Parse(payload, self.context)[0]
                if ('object_id' in values):
                    note = self.context.run_command('note::get', id=values['object_id'])
                elif (self.has_child(request_name)): note = self.get_child(request_name)
                else: note = None
            else:
                # WebDAV Mode (file operations)
                values = None
                if (self.has_child(request_name)): note = self.get_child(request_name)
                else: note = None
            # Perform operations
            if (note is None):
                print '___CREATE____'
                # create
                if (values is None):
                    # file create
                    note = self.context.run_command('note::new', values={'title': request_name,
                                                                         'projectId': self.entity.object_id },
                                                                 text=payload,
                                                                 context=self.entity)
                else:
                    # vjournal create
                    note = self.context.run_command('note::new', values=values,
                                                                 context=self.entity)
                    print 'setting caldav_uid = {0}'.format(request_name)
                    note.caldav_uid = request_name
                self.request.send_response(201, 'Created')
                self.request.send_header('Etag', u'{0}:{1}'.format(note.object_id, note.version))
                self.request.send_header('Content-Type', u'{0}; charset=utf-8'.format(mimetype))
                self.request.send_header('Location', u'{0}/{1}'.format(self.get_path(), request_name))
                self.request.end_headers()
            else:
                print '___UPDATE____'
                # update
                if (values is None):
                    # file update
                    note = self.context.run_command('note::set', object=note,
                                                                 context=self.entity,
                                                                 text=payload)
                else:
                    # vjournal update
                    note = self.context.run_command('note::set', object=note,
                                                                 context=self.entity,
                                                                 values=values)
            self.context.commit()
            print '________________'
            print note.title
            print note.categories
            print note.created
            print '________________'
            self.request.send_response(204, 'Updated, no content.')
            self.request.send_header('Etag', u'{0}:{1}'.format(note.object_id, note.version))
            self.request.send_header('Content-Type', u'{0}; charset=utf-8'.format(mimetype))
            self.request.send_header('Location', u'{0}/{1}'.format(self.get_path(), request_name))
            self.request.end_headers()

    def do_REPORT(self):
        ''' Preocess a report request '''
        payload = self.request.get_request_payload()
        self.log.debug('REPORT REQUEST: %s' % payload)
        parser = Parser.report(payload)
        if (parser.report_name == 'calendar-query'):
            self._start = parser.parameters.get('start', None)
            self._end   = parser.parameters.get('end', None)
            d = {}
            if (self.load_contents()):
                # TODO: Do VJOURNAL objects need CalDAV UID support
                for note in self.get_children():
                    name = u'{0}.vjl'.format(note.object_id)
                    x = NoteObject(self, name, entity=note,
                                               location=u'{0}/{1}'.format(self.url, name),
                                               request=self.request,
                                               context=self.context)
                    d[x.location] = x
                self.request.send_response(207, 'Multistatus')
                self.request.send_header('Content-Type', 'text/xml')
                w = BufferedWriter(self.request.wfile, False)
                Multistatus.generate(d, parser.properties, w)
                self.request.send_header('Content-Length', str(w.getSize()))
                self.request.end_headers()
                w.flush()
        elif (parser.report_name == 'calendar-multiget'):
            d = {}
            if (self.load_contents()):
                for href in parser.references:
                    if (href not in d):
                        key = href.split('/')[-1]
                        try:
                            entity = self.get_object_for_key(key)
                            d[href] = entity
                        except NoSuchPathException, e:
                            self.log.debug('Missing resource {0} in collection'.format(key))
                        except Exception, e:
                            self.log.exception(e)
                            raise e
                self.request.send_response(207, 'Multistatus')
                self.request.send_header('Content-Type', 'text/xml')
                w = BufferedWriter(self.request.wfile, False)
                Multistatus.generate(d, parser.properties, w)
                self.request.send_header('Content-Length', str(w.getSize()))
                self.request.end_headers()
                w.flush()
        else:
            raise CoilsException('Unsupported report {0} in {1}'.format(parser.report_name, self))

    def do_DELETE(self, name):
        if (self.load_contents()):
            if (self.has_child(name)):
                # TODO: Catch exceptions and return an appropriate error
                self.context.run_command('contact::delete', object=self.get_child(name))
                self.context.commit()
                self.request.send_response(204, 'No Content')
                self.request.end_headers()
            else:
                self.no_such_path()
        else:
            raise CoilsException('Unable to enumerate collection contents.')
