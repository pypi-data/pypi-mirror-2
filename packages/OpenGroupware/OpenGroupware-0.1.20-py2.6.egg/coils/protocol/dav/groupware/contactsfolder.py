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
import sys, coils.core
from coils.core                        import *
from coils.core.vcard                  import Parser as VCard_Parser
from coils.foundation                  import CTag, Contact
from coils.protocol.dav.foundation     import DAVFolder, \
                                                DAVObject, \
                                                OmphalosCollection, \
                                                OmphalosObject

class ContactsFolder(DAVFolder):
    def __init__(self, parent, name, **params):
        DAVFolder.__init__(self, parent, name, **params)

    def supports_GET(self):
        return False

    def supports_POST(self):
        return False

    def supports_PUT(self):
        return True

    def supports_DELETE(self):
        return True

    def supports_PROPFIND(self):
        return True

    def supports_PROPATCH(self):
        return False

    def supports_MKCOL(self):
        return False

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
        query = db.query(CTag).filter(CTag.entity=='Person')
        ctags = query.all()
        if (len(ctags) == 0):
            return None
        query = None
        return ctags[0].ctag

    def _load_self(self):
        self.data = { }
        content = self.context.run_command('contact::list', properties = [ Contact ])
        #content = self.context.run_command('contact::list', properties = [ Contact ], limit=25 )
        if (content is not None):
           for ls_entry in content:
               self.data['{0}.vcf'.format(ls_entry.object_id)] = ls_entry
        else:
            return False
        return True

    def _get_contact_for_key(self, key):
        # If we are PROPFIND'ing the folder we already will have the Contacts listed in
        # the object, so we really don't want to do a one-by-one load.  One caveat is
        # that we will not have the Contact's comment value.  That should probably be
        # fixed in the ORM.
        if (self.data is not None):
            if (key in self.data):
                return self.data[key]
        try:
            object_id = int(str(key).split('.')[0])
        except:
            return None
        return self.context.run_command('contact::get', id=object_id)

    def object_for_key(self, name):
        if ((name == '.json') and (self.load_self())):
            return OmphalosCollection(self,
                                       name,
                                       data=self.data.values(),
                                       context=self.context,
                                       request=self.request)
        elif (name[:11] == '.birthdays.'):
            result = self.context.run_command('contact::get-upcoming-birthdays')
            return OmphalosCollection(self,
                                       name,
                                       rendered=True,
                                       data=result,
                                       context=self.context,
                                       request=self.request)
        elif ((name[-4:] == '.vcf') or
              (name[-5:] == '.json') or
              (name[-4:] == '.xml') or
              (name[-5:] == '.yaml')):
            entity = self._get_contact_for_key(name)
            if (entity is not None):
                if (name[-4:] == '.vcf'):
                    return DAVObject(self,
                                      name,
                                      entity=entity,
                                      context=self.context,
                                      request=self.request)
                else:
                    return OmphalosObject(self,
                                           name,
                                           entity=entity,
                                           context=self.context,
                                           request=self.request)
        self.no_such_path()

    def do_PUT(self, name):
        contact = self._get_contact_for_key(name)
        values = None
        if (contact is not None):
            object_id = contact.object_id
        else:
            object_id = None
        if_etag = self.request.headers.get('If-Match', None)
        if (if_etag is None):
            self.log.warn('Client issued a put operation with no If-Match!')
        payload = self.request.get_request_payload()
        values = VCard_Parser.Parse(payload, self.context, entity_name='Contact')
        if (values):
            data = values[0]
            if ('object_id' in data):
                if (object_id is None):
                    object_id = data['object_id']
                elif (object_id != data['object_id']):
                    #TODO: Huh?
                    pass
            if (object_id is None):
                a = self.context.run_command('contact::new', values=data)
                self.context.commit()
                self.request.send_response(201, 'Created')
                self.request.send_header('Etag', '{0}:{1}'.format(a.object_id, a.version))
                self.request.send_header('Location', '/dav/Contacts/{0}.ics'.format(a.object_id))
                self.request.end_headers()
            else:
                try:
                    contact = self.context.run_command('contact::get', id=object_id)
                    if (contact is None):
                        self.log.error('Unable to marshal objectId#{0} for update via WebDAV'.format(object_id))
                        raise CoilsException('Unable to marshal contact for update (permissions?)')
                    try:
                        contact = self.context.run_command('contact::set', object=contact, values=data)
                    except Exception, e:
                        self.log.error('Error updating objectId#{0} via WebDAV'.format(object_id))
                        self.log.exception(e)
                        raise e
                    self.context.commit()
                except:
                    raise CoilsException('Contact update failed.')
                else:
                    self.request.send_response(204, 'No Content')
                    self.request.send_header('Etag', '{0}:{1}'.format(contact.object_id, contact.version))
                    self.request.end_headers()

    def do_DELETE(self, name):
        contact = self._get_contact_for_key(name)
        values = None
        if (contact is None):
            self.no_such_path()
        try:
            self.context.run_command('contact::delete', object=contact)
            self.context.commit()
        except:
            self.request.send_response(500, 'Deletion failed')
        else:
            self.request.send_response(204, 'No Content')
        self.request.end_headers()
