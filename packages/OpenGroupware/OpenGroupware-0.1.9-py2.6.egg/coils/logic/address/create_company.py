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
#
from datetime         import datetime, timedelta
from pytz             import timezone
from sqlalchemy       import *
from sqlalchemy.orm   import *
from coils.foundation import *
from coils.core       import *
from coils.core.logic import CreateCommand
from keymap           import COILS_TELEPHONE_KEYMAP, COILS_ADDRESS_KEYMAP

class CreateCompany(CreateCommand):

    def __init__(self):
        CreateCommand.__init__(self)
        self.sd = ServerDefaultsManager()

    def _initialize_addresses(self, kinds):
        # TODO: Read defined address types from config
        x = KVC.subvalues_for_key(self.values, ['_ADDRESSES', 'addresses'])
        addresses = KVC.keyed_values(x, ['kind', 'type'])
        for kind in kinds:
            if (kind in addresses):
                values = addresses[kind]
            else:
                values = { }
            address = self._ctx.run_command('address::new', values=values,
                                                            parent_id=self.obj.object_id,
                                                            kind=kind)

    def _initialize_telephones(self, kinds):
        # TODO: Read define phone number types from config
        x = KVC.subvalues_for_key(self.values, ['_PHONES', 'telephones', 'phones'])
        telephones = KVC.keyed_values(x, ['kind', 'type'])
        for kind in kinds:
            if (kind in telephones):
                values = telephones[kind]
            else:
                values = { }
            telephone = self._ctx.run_command('telephone::new', values=values,
                                                                parent_id=self.obj.object_id,
                                                                kind=kind)

    def _list_subtypes_types_for_entity(self, default_name):
        subtypes = self.sd.default_as_dict(default_name)
        if (self.obj.__internalName__ in subtypes):
            if (isinstance(subtypes[self.obj.__internalName__], list)):
                return subtypes[self.obj.__internalName__]
            else:
                raise CoilsException(
                    'Sub-type list {0} in default {1} is improperly structured'.format(
                        self.obj.__internalName__,
                        default_name))
        raise CoilsException(
            'Not sub-type list defined in default {0} for entity type {1}'.format(
                default_name,
                str(self.obj)))

    def set_comment_text(self):
        if ('comment' in self.values):
            self._ctx.run_command('company::set-comment-text', company=self.obj,
                                                               text=self.values['comment'])

    def run(self):
        CreateCommand.run(self)
        types = self._list_subtypes_types_for_entity('LSAddressType')
        self._initialize_addresses(types)
        types = self._list_subtypes_types_for_entity('LSTeleType')
        self._initialize_telephones(types)
        self.obj.number = 'OGo{0}'.format(self.obj.object_id)
        self.obj.login = 'OGo{0}'.format(self.obj.object_id)
        self.set_comment_text()
