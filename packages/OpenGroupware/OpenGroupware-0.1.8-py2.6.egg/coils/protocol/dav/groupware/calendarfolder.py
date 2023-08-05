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
from datetime                          import datetime, timedelta
from coils.foundation                  import CTag, ServerDefaultsManager
from coils.core                        import Appointment, NoSuchPathException
import  coils.core.icalendar
from coils.protocol.dav.foundation     import DAVFolder, \
                                                OmphalosCollection, \
                                                OmphalosObject, \
                                                Parser, \
                                                BufferedWriter, \
                                                Multistatus
from eventobject                       import EventObject


class CalendarFolder(DAVFolder):
    def __init__(self, parent, name, **params):
        DAVFolder.__init__(self, parent, name, **params)
        self._start = None
        self._end   = None

    def _get_event_for_key(self, key):
        key = str(key).split('.')[0]
        if (key.isdigit()):
            object_id = int(key)
            return self.context.run_command('appointment::get', id=object_id)
        else:
            return None

    def _get_overview_range(self, **params):
        events = self.context.run_command('appointment::get-overview-range', **params)
        return events

    def _get_personal_range(self, **params):
        events = self.context.run_command('appointment::get-range', **params)
        return events

    def _get_calendar_range(self, **params):
        events = self.context.run_command('appointment::get-calendar', **params)
        return events

    # PROP: GETCTAG

    def get_property_unknown_getctag(self):
        return self.get_property_caldav_getctag()

    def get_property_webdav_getctag(self):
        return self.get_property_caldav_getctag()

    def get_property_caldav_getctag(self):
        return self.get_ctag()

    def get_ctag(self):
        ''' Return a ctag appropriate for this object.
            Actual WebDAV objects should override this method '''
        db = self.context.db_session()
        query = db.query(CTag).filter(CTag.entity=='Date')
        ctags = query.all()
        if (len(ctags) == 0):
            return None
        query = None
        return ctags[0].ctag

    def _load_self(self):
        # TODO: Read range from server configuration
        self.log.info('Loading content in calendar folder for name {0}'.format(self.name))
        if (self._start is None):
            self._start = datetime.now() - timedelta(days=1)
        if (self._end is None):
            self._end   = datetime.now() + timedelta(days=90)
        result = None
        if (self.name == 'Calendar'):
            self.data = { 'Personal': CalendarFolder(self, 'Personal', context=self.context, request=self.request),
                          'Overview': CalendarFolder(self, 'Overview', context=self.context, request=self.request) }
            ud = ServerDefaultsManager()
            calendars = ud.default_as_list('LSCalendars')
            for calendar in calendars:
                self.data[calendar] = CalendarFolder(self, calendar, context=self.context, request=self.request)
            return True
        elif (self.name == 'Personal'):
            events = self._get_personal_range(start = self._start,
                                              end   = self._end)
        elif (self.name == 'Overview'):
            events = self._get_overview_range(start = self._start,
                                              end   = self._end)
        else:
            events = self._get_calendar_range(calendar = self.name,
                                              start    = self._start,
                                              end      = self._end)
        if (events is not None):
            self.data = { }
            for event in events:
                self.data['{0}.ics'.format(event.object_id)] = event
            return True
        return False

    def object_for_key(self, name):
        if (self.load_self()):
            if (self.name == 'Calendar'):
                # Calendar root folder
                if ((name[-4:] == '.ics') or (name[-5:] == '.json')):
                    if (name.split('.')[0].isdigit()):
                        event = self._get_event_for_key(name)
                        if (event is not None):
                            if (name[-5:] == '.json'):
                                return OmphalosObject(self,
                                                       name,
                                                       entity=event,
                                                       context=self.context,
                                                       request=self.request)
                            else:
                                return EventObject(self,
                                                    name,
                                                    entity=event,
                                                    context=self.context,
                                                    request=self.request)
                else:
                    return self.data[name]
            else:
                # Calendar sub-folder
                if (name == '.json'):
                    return OmphalosCollection(self,
                                               name,
                                               data=self.data.values(),
                                               context=self.context,
                                               request=self.request)
                elif ((name[-4:] == '.ics') or (name[-5:] == '.json')):
                    if (name[-4:] == '.ics'):
                        if (name in self.data):
                            return EventObject(self, name, entity=self.data[name],
                                                            location='/dav/Calendar/{0}'.format(name),
                                                            context=self.context,
                                                            request=self.request)
                    elif (name[-5:] == '.json'):
                        name = '{0}.ics'.format(name[:-5])
                        if (name in self.data):
                            return OmphalosObject(self,
                                                   name,
                                                   entity=self.data[name],
                                                   context=self.context,
                                                   request=self.request)
            self.no_such_path()
        raise CoilsException('Folder contents failed to load')

    def supports_PUT(self):
        return True

    def supports_DELETE(self):
        return True        

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
        self.request.send_header('DAV', '1, calendar-access')
        self.request.send_header('MS-Author-Via', 'DAV')
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
            if (self.load_self()):
                for name in self.data:
                    x = EventObject(self, name, entity=self.data[name][0],
                                                location='/dav/Calendar/{0}'.format(name),
                                                context=self.context,
                                                request=self.request)
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
            if (self.load_self()):
                for href in parser.references:
                    if (href not in d):
                        key = href.split('/')[-1]
                        try:
                            entity = self.object_for_key(key)
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

    def do_PUT(self, name):
        ''' Process a PUT request '''
        self.log.debug('PUT request with name {0}'.format(name))
        event = self._get_event_for_key(name)
        if (event is not None):
            object_id = event.object_id
        else:
            object_id = None
        if_etag = self.request.headers.get('If-Match', None)
        if (if_etag is None):
            self.log.warn('Client issued a put operation with no If-Match!')
        payload = self.request.get_request_payload()
        values = coils.core.icalendar.Parser.Parse(payload, self.context)
        if (values):
            data = values[0]
            if (('object_id' in data) and (object_id is None)):
                object_id = data['object_id']
            if (object_id is None):
                a = self.context.run_command('appointment::new', values=data)
                self.context.commit()
                self.request.send_response(201, 'Created')
                self.request.send_header('Etag', '{0}:{1}'.format(a.object_id, a.version))
                self.request.send_header('Location', '/dav/Calendar/{0}.ics'.format(a.object_id))
                self.request.end_headers()
            else:
                a = self.context.run_command('appointment::get', id=data['object_id'])
                a = self.context.run_command('appointment::set', object=appointment,
                                                                 values=data)
                self.context.commit()
                self.request.send_response(204, 'No Content')
                self.request.send_header('Etag', '{0}:{1}'.format(a.object_id, a.version))
                self.request.end_headers()
