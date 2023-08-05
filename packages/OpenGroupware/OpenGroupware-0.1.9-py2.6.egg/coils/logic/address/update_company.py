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
import pprint
from sqlalchemy       import *
from coils.core       import *
from coils.core.logic import UpdateCommand
from keymap           import COILS_TELEPHONE_KEYMAP, COILS_ADDRESS_KEYMAP

class UpdateCompany(UpdateCommand):

    def __init__(self):
        UpdateCommand.__init__(self)
        self.sd = ServerDefaultsManager()

    def parse_parameters(self, **params):
        UpdateCommand.parse_parameters(self, **params)

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

    def _update_company_values(self):
        if ('_COMPANYVALUES' not in self.values):
            return
        x = KVC.subvalues_for_key(self.values, ['_COMPANYVALUES'])
        company_values = KVC.keyed_values(x, ['attribute'])
        for attribute in company_values:
            for value in self.obj.company_values:
                if (value.name == attribute):
                    x = company_values[attribute].get('value', None)
                    if (x is None):
                        value.string_value = None
                        value.integer_value = None
                    else:
                        x = str(x)
                        value.string_value = x
                        if (x.isdigit()):
                            value.integer_value = int(x)
                        else:
                            value.integer_value = None
                    break

    def _update_telephones(self, kinds):
        x = KVC.subvalues_for_key(self.values, ['_PHONES', 'telephones', 'phones'])
        telephones = KVC.keyed_values(x, ['kind', 'type'])
        for kind in telephones:
            telephone = KVC.translate_dict(telephones[kind], COILS_TELEPHONE_KEYMAP)
            # Silently filter out telephones of unknown kinds
            if (kind in kinds):
                self._ctx.run_command('telephone::set', values=telephone,
                                                        kind=kind,
                                                        parent_id=self.obj.object_id)

    def _update_addresses(self, kinds):
        x = KVC.subvalues_for_key(self.values, ['_ADDRESSES', 'addresses'])
        addresses = KVC.keyed_values(x, ['kind', 'type'])
        for kind in addresses:
            address = addresses.get(kind)
            address = KVC.translate_dict(address, COILS_ADDRESS_KEYMAP)
            # Silently filter out addresses of unknown kinds
            if (kind in kinds):
                self._ctx.run_command('address::set', values=address,
                                                      kind=kind,
                                                      parent_id=self.obj.object_id)
            else:
                print 'no such address kind as {0}'.format(kind)

    def set_comment_text(self):
        comment_text = self.values.get('comment', None)
        if (comment_text is not None):
            self._ctx.run_command('company::set-comment-text', parent_id=self.obj.object_id,
                                                               text=self.values['comment'])

    def run(self):
        UpdateCommand.run(self)
        kinds = self._list_subtypes_types_for_entity('LSTeleType')
        self._update_telephones(kinds)
        kinds = self._list_subtypes_types_for_entity('LSAddressType')
        self._update_addresses(kinds)
        self._update_company_values()
        self.set_comment_text()