#!/usr/bin/python
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
import io, os
from log import *
import ConfigParser, logging
from sqlalchemy                 import *
from sqlalchemy.orm             import sessionmaker
from coils.foundation           import *
from defaultsmanager            import DefaultsManager

Session = sessionmaker()

def _parse_default_as_bool(value):
    if (values is None):
        return False
    if (values == 'YES'):
        return True
    return False

class Backend(object):
    _engine   = None
    _config   = None
    _session  = None
    _auth     = None
    _fs_url   = None
    _log      = None
    _defaults = None

    @staticmethod
    def __alloc__(**params):
        if (Backend._config is None):
            # TODO: Allow to be modified
            Backend._store_root = params.get('store_root', '/var/lib/opengroupware.org')
            Backend._fs_url = '{0}/fs'.format(DefaultsManager._store_root)
            DefaultsManager._store_root = Backend._store_root
            # Open defaults
            sd = ServerDefaultsManager()

            # TODO: Read from defaults
            log_filename = params.get('log_file', '/var/log/coils.log')
            log_level = LEVELS.get('DEBUG', logging.NOTSET)
            logging.basicConfig(filename=log_filename, level=log_level)
            Backend._log = logging
            logging.debug('Backend initialized')

    def __init__(self, **params):
        if (Backend._config is None):
            Backend.__alloc__(**params)

    @staticmethod
    def _parse_default_as_bool(value):
        if (values is None):
            return False
        if (values == 'YES'):
            return True
        return False

    @staticmethod
    def db_session():
        if (Backend._engine is None):
            sd = ServerDefaultsManager()
            Backend._engine = create_engine(sd.orm_dsn, **{'echo': sd.orm_logging})
            Session.configure(bind=Backend._engine)
        #session = Session()
        return Session()
        #return Backend._session

    @staticmethod
    def get_logic_bundle_names():
        #TODO: Load from config
        return [ 'coils.logic.account', 'coils.logic.address',
                  'coils.logic.blob', 'coils.logic.contact',
                  'coils.logic.enterprise', 'coils.logic.facebook',
                  'coils.logic.project', 'coils.logic.pubsub',
                  'coils.logic.schedular', 'coils.logic.task',
                  'coils.logic.team', 'coils.logic.twitter',
                  'coils.logic.workflow', 'mormail.hedera' ]
        #bundle_names = [ ]
        #for name in Backend._config.get('globals', 'logic_bundles').split(','):
        #    bundle_names.append(name.strip())
        #return bundle_names

    @staticmethod
    def get_protocol_bundle_names():
        #TODO: Load from config
        return [ 'coils.protocol.dav', 'coils.protocol.freebusy',
                  'coils.protocol.proxy', 'coils.protocol.zogi' ]
        #bundle_names = [ ]
        #for name in Backend._config.get('globals', 'protocol_bundles').split(','):
        #    bundle_names.append(name.strip())
        #return bundle_names

    @staticmethod
    def store_root():
        return Backend._store_root

    @staticmethod
    def fs_root():
        return Backend._fs_url

    @staticmethod
    def get_authenticator_options():
        #TODO: Reimplement sensing LDAP configuration and populating to dictionary.
        return { 'authentication': 'db' }
        # LDAPAuthentication expects:
        #   start_tls : YES / NO
        #   binding : SIMPLE, DIGEST
        #   bind_identity, bind_secret
        #   search_container, search_filter, uid_attribute

    @staticmethod
    def get_section_options(section):
        result = { }
        if (Backend._config.has_section(section)):
            for option in Backend._config.options(section):
                result[option] = Backend._config.get(section, option)
        return result
