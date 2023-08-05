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
from datetime                          import datetime
# DAV Classses
from coils.protocol.dav.foundation     import DAVObject, DAVFolder

class AccountsFolder(DAVFolder):
    def __init__(self, parent, name, **params):
        DAVFolder.__init__(self, parent, name, **params)

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
        try:
            accounts = self.context.run_command('account::get-all')
            for account in accounts:
                #self.data['{0}.vcf'.format(account.object_id)] = [account]
                self.data['{0}.vcf'.format(account.login)] = [account]
        except Exception, e:
            self.log.exception(e)
            return False
        else:
            return True

    def object_for_key(self, name):
        if (self.load_self()):
            if (name in self.data):
                entity = self.data[name][0]
                return DAVObject(self, name, entity=entity,
                                              location='/dav/Contacts/{0}.vcf'.format(entity.object_id),
                                              context=self.context,
                                              request=self.request)
        return self.no_such_path()