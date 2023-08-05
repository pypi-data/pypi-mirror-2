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
# THE SOFTWARE.
#
import sys, time, logging
from sqlalchemy        import *
from pytz              import timezone
from datetime          import datetime, timedelta
from coils.foundation  import *
from exception         import *
from ldapauthenticator import LDAPAuthenticator
from dbauthenticator   import DBAuthenticator
from bundlemanager     import BundleManager
from accessmanager     import AccessManager
from linkmanager       import LinkManager
from propertymanager   import PropertyManager
from command           import Command
from packet            import Packet

class Context(object):
    _typeManager   = None
    _mapper        = None
    _accessManager = None
    _orm           = None

    def __init__(self, metadata, broker=None):
        self.transaction = None
        self.orm = None
        self.am = None  # Access Manager
        self.lm = None  # Link Manager
        self.pm = None  # Property Manager
        self.log = logging.getLogger('context')
        self._email = None
        self.metadata = metadata
        if (Context._typeManager == None):
            Context._typeManager = TypeManager()
        if (Context._mapper == None):
            Context._mapper = BundleManager()
        if (Context._accessManager == None):
            Context._accessManager = AccessManager()
        if ('amq_broker' not in metadata) and (broker is None):
            self.log.debug('AMQ broker not available in context.')
        else:
            self.metadata['amq_broker'] = metadata.get('amq_broker', broker)

    def __del__(self):
        self.close()

    def close(self):
        self.log.debug('Closing context.')
        if (self.orm is not None):
            self.orm.close()
            self.orm = None

    def type_manager(self):
        return Context._typeManager

    def access_manager(self):
        return Context._accessManager

    def link_manager(self):
        if (self.lm is None):
            self.lm = LinkManager(self)
        return self.lm

    @property
    def property_manager(self):
        if (self.pm is None):
            self.pm = PropertyManager(self)
        return self.pm

    def db_session(self):
        if (self.orm is None):
            self.log.debug('Allocating new database session.')
            self.orm = Backend.db_session()
        return self.orm

    def begin(self):
        #if (self.transaction == None):
        #    self.transaction = self.db_session.create_transaction()
        pass

    def commit(self):
        #self.db_session.flush()
        self.log.debug('Context commit requested.')
        self.db_session().commit()
        self.log.debug('Context commit completed.')
        return
        if (transaction == None):
            raise Exception('Attempt to commit without a transaction')
        try:
            self.db_session.flush()
            self.transaction.commit()
        except:
            raise
        finally:
            self.transaction = None

    def rollback(self):
        self.db_session().rollback()
        return
        if (self.transaction == None):
            raise Exception('Attempt to rollback without a transaction')
        try:
            self.transaction.rollback()
        except:
            raise
        finally:
            self.transaction = None

    def run_command(self, command_name_x, **params):
        command = Context._mapper.get_command(command_name_x)
        if isinstance(command, Command):
            start = time.time()
            command.prepare(self, **params)
            command.run()
            command.epilogue()
            result = command.get_result()
            end = time.time()
            self.log.debug('duration of %s was %0.3f' % (command_name_x, (end - start)))
            command = None
            return result
        else:
            self.log.error('No such command as {0}'.format(command_name_x))
            raise CoilsException('No such command as {0}'.format(command_name_x))
        return None

    @property
    def defaults(self):
        return self.get_defaults()

    def get_defaults(self):
        return {}

    def get_timezone(self):
        return timezone('UTC')

    def get_utctime(self):
       utc = timezone('UTC')
       return datetime.now(tz=utc)

    def as_localtime(self, time):
        if (time is None):
            return self.get_localtime()
        return time.astimezone(self.get_timezone())

    def get_offset_from(self, time):
        return ((86400 - self.get_timezone().utcoffset(time).seconds) * -1)

    def get_locatime(self):
       tz = self.get_timezone()
       localtime = self.get_utctime().astimezone(tz)

    @property
    def login(self):
        return self.get_login()

    def get_login(self):
        return None

    @property
    def email(self):
        if (self._login is None):
            return None
        if (self._email is None):
            if (hasattr(self._login, 'company_values')):
                for cv in self._login.company_values:
                    if (cv.name == 'email1'):
                        if (cv.string_value is not None):
                            if (len(cv.string_value) > 0):
                                self._email = cv.string_value
        return self._email

    @property
    def amq_broker(self):
        return self.metadata['amq_broker']

    @property
    def amq_available(self):
        if ('amq_broker' in self.metadata):
            return True
        return False

    def send(self, source, target, data):
        if (self.amq_available):
            packet = Packet(source, target, data)
            self.amq_broker.send(packet)
        else:
            raise CoilsException('Service bus not available to context.')


class AnonymousContext(Context):
    def __init__(self, metadata = {}, broker=None):
        Context.__init__(self, metadata, broker=broker)

    @property
    def account_id(self):
        return 0

    @property
    def context_ids(self):
        return [0]

    def get_login(self):
        return 'Coils\\Anonymous'


class AdministrativeContext(Context):

    def __init__(self, metadata = {}, broker=None):
        Context.__init__(self, metadata, broker=broker)

    @property
    def account_id(self):
        return 10000

    @property
    def context_ids(self):
        return [ 10000 ]

    def get_login(self):
        return 'Coils\\Administrator'


class AuthenticatedContext(Context):
    _auth_class   = None
    _auth_options = None
    _defaults     = None
    _timezone     = None
    _context_ids  = None

    def __init__(self, metadata, broker=None):
        Context.__init__(self, metadata, broker=broker)
        if (AuthenticatedContext._auth_options is None):
            AuthenticatedContext._auth_options = Backend.get_authenticator_options()
        if (AuthenticatedContext._auth_class is None):
            class_name = '%sAuthenticator' % AuthenticatedContext._auth_options['authentication'].upper()
            AuthenticatedContext._auth_class = eval(class_name)
        Backend._log.debug('Authentication class is {0}'.format(AuthenticatedContext._auth_class))
        self.authorizor = AuthenticatedContext._auth_class(self,
                                                           self.metadata,
                                                           AuthenticatedContext._auth_options)
        if (self.authorizor.authenticated_id() is None):
            self.log.warn('Unable to authenticate sessoion')
            raise AuthenticationException('Unable to authenticate session')

    def get_login(self):
        return self.metadata['authentication']['login']

    def get_defaults(self):
        if (self._defaults is None):
            self._defaults = self.run_command('account::get-defaults')
        return self._defaults

    def get_timezone(self):
        if (self._timezone is None):
            defaults = self.get_defaults()
            if (defaults.has_key('timezone')):
                self._timezone = timezone(defaults['timezone'])
            else:
                self._timezone = timezone('UTC')
        return self._timezone

    @property
    def account_id(self):
        return self.authorizor.authenticated_id()

    @property
    def context_ids(self):
        if (self._context_ids is None):
            self._context_ids = []
            self._context_ids.append(self.account_id)
            x = self.run_command('team::get', member_id = self.account_id)
            for team in x:
                self._context_ids.append(team.object_id)
        return self._context_ids


class AssumedContext(Context):
    _defaults     = None
    _timezone     = None
    _context_ids  = None

    def __init__(self, context_id, metadata = {}, broker=None):
        Context.__init__(self, metadata, broker=broker)
        self._get_login(context_id)

    def _get_login(self, context_id):
        db = self.db_session()
        query = db.query(Contact).filter(and_(Contact.object_id==context_id,
                                               Contact.is_account==1,
                                               Contact.status!='archived'))
        data = query.first()
        if (data is not None):
            self._login = data
        else:
            raise AuthenticationException('No account with id of {0}.'.format(context_id))

    def get_login(self):
        return self._login.login

    def get_defaults(self):
        if (self._defaults is None):
            self._defaults = self.run_command('account::get-defaults')
        return self._defaults

    def get_timezone(self):
        if (self._timezone is None):
            defaults = self.get_defaults()
            if (defaults.has_key('timezone')):
                self._timezone = timezone(defaults['timezone'])
            else:
                self._timezone = timezone('UTC')
        return self._timezone

    @property
    def account_id(self):
        return self._login.object_id

    @property
    def context_ids(self):
        if (self._context_ids is None):
            self._context_ids = []
            self._context_ids.append(self.account_id)
            x = self.run_command('team::get', member_id = self.account_id)
            for team in x:
                self._context_ids.append(team.object_id)
        return self._context_ids
