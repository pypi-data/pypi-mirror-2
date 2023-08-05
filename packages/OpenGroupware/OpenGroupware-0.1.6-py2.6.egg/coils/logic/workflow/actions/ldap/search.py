#
# Copyright (c) 2010 Adam Tauno Williams <awilliam@whitemice.org>
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
#
import os, ldap
from coils.core              import *
from coils.core.logic        import ActionCommand
from dsml1_writer            import DSML1Writer

class SearchAction(ActionCommand):
    __domain__    = "action"
    __operation__ = "ldap-search"
    __aliases__   = [ 'ldapSearch', 'ldapSearchAction' ]

    def __init__(self):
        ActionCommand.__init__(self)

    def do_action(self):
        dsa = LDAPConnectionFactory.Connect(self._dsa)
        if (len(self._attrs) == 0):
            self.attrs = None
        try:
            results = dsa.search_s(self._root,
                                   self._scope,
                                   self._filter,
                                   self._attrs)
        except ldap.NO_SUCH_OBJECT, e:
            self.log.exception(e)
            self.log.info('LDAP NO_SUCH_OBJECT exception, generating empty message')
        except ldap.INSUFFICIENT_ACCESS, e:
            self.log.exception(e)
            self.log.info('LDAP INSUFFICIENT_ACCESS exception, generating empty message')
        except ldap.SERVER_DOWN, e:
            self.log.exception(e)
            self.log.warn('Unable to contact LDAP server!')
            raise e
        except Exception, e:
            self.log.error('Exception in action ldapSearch')
            self.log.exception(e)
            raise e
        else:
            writer = DSML1Writer()
            writer.write(results, self._wfile)
        dsa.unbind()

    def parse_action_parameters(self):
        self._dsa    = self._params.get('dsaName',     None)
        self._filter = self._params.get('filterText',  None)
        self._root   = self._params.get('searchRoot',  None)
        self._scope  = self._params.get('searchScope', 'SUBTREE').upper()
        self._limit  = self._params.get('searchLimit', 150)
        self._attrs  = self._params.get('attributes', '').split(',')
        if (self._dsa is None):
            raise CoilsException('No DSA defined for ldapSearch')
        # Check query value
        if (self._filter is None):
            raise CoilsException('No filter defined for ldapSearch')
        else:
            self._filter = self.decode_text(self._filter)
            self.log.debug('LDAP FILTER:{0}'.format(self._filter))
        # Check root parameter
        if (self._root is None):
            raise CoilsException('No root defined for ldapSearch')
        else:
            self._root = self.decode_text(self._root)
        # Convert subtree parameter
        if (self._scope == 'SUBTREE'):
            self._scope = ldap.SCOPE_SUBTREE
        else:
            self._scope = ldap.SCOPE_SUBTREE

    def do_epilogue(self):
        pass