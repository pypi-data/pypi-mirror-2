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
# THE SOFTWARE.
#
import vobject, datetime, pytz, re, pprint


def take_integer_value(values, key, name, vcard, default=None):
    key = key.replace('-', '_')
    if (hasattr(vcard.key)):
        try:
            values[name] = int(getattr(vcard, key).value)
        except:
            values[name] = default

def take_string_value(values, key, name, vcard, default=None):
    key = key.replace('-', '_')
    if (hasattr(vcard.key)):
        try:
            values[name] = str(getattr(vcard, key).value)
        except:
            values[name] = default


def determine_adr_type(attributes, **params):
    # Is the X-EVOLUTION-UI-SLOT=1 attribute usefule in any way? Can
    # we at least preserve that as an object property?
    if ('X-COILS-ADDRESS-TYPE' in attributes):
       return attributes['X-COILS-ADDRESS-TYPE'][0]
    elif ('TYPE' in attributes):
        # ADR element does not contain a X-COILS-ADDRESS-TYPE property
        # so we need to generate an OGo address type from the vCard
        # TYPE params
        #
        if (entity_name == 'Contact'):
            if ('home' in attributes):
                return 'private'
            elif ('work' in attributes):
                return 'mailing'
            else:
                return 'location'
        elif (entity_name == 'Enterprise'):
            #TODO: Implement
            raise NotImplementedException()
        elif (entity_name == 'Team'):
            # Addresses in Team vCards are discarded
            return None
        else:
            # It isn't a Contact, Team, or Enterprise?
            raise CoilException('Unknown vCard to entity correspondence')
    else:
        raise CoilsException('Cannot parse vCard; address with no type')

def parse_vcard(card, ctx, log, **params):
    entity_name = params.get('entity_name', 'Contact')
    if (entity_name not in ['Contact', 'Enterprise']):
        raise CoilsException('Parsing to this kind of entity not supported.')
    values = {}
    emails = []
    for line in card.lines():
        if line.name == 'UID':
            # UID
            # Try to dig the objectId out of the UID
            if (line.value[:8] == 'coils://'):
                if ((entity_name == 'Contact') and
                    (line.value[:16] == 'coils://Contact/') and
                    line.value[16:].isdigit()):
                    values['objectId'] = int(line.value[16:])
                elif ((entity_name == 'Enterprise') and
                      (line.value[:19] == 'coils://Enterprise/') and
                      (line.value[19:].isdigit())):
                    values['objectId'] = int(line.value[19:])
                elif ((entity_name == 'Team') and
                      (line.value[:13] == 'coils://Team/') and
                      (line.value[13:].isdigit())):
                    values['objectId'] = int(line.value[13:])
                else:
                   log.warn('Corrupted COILS UID String: {0}'.format(line.value))
            else:
                log.debug('vCard UID not a COILS id: {0}'.format(line.value))
        elif line.name == 'ADR':
            # ADR (Postal Address)
            # TODO: It is always good to make this more intelligent
            kind = determine_adr_type(line.params, **params)
            # If kind is None the address is discarded [on purpose, not a bug]
            if (kind is not None):
                if ('_ADDRESSES' not in values):
                    values['_ADDRESSES'] = [ ]
                address = {'type': kind }
                address['name1']      = line.value.extended
                address['city']       = line.value.city
                address['postalCode'] = line.value.code
                address['country']    = line.value.country
                address['state']      = line.value.region
                address['street']     = line.value.street
                values['_ADDRESSES'].append(address)
        elif line.name == 'X-JABBER':
            values['imAddress'] = line.value
        elif line.name == 'TITLE':
            if '_COMPANYVALUES' not in values:
                values['_COMPANYVALUES'] = [ ]
            values['_COMPANYVALUES'].append({'attribute': 'job_title', 'value': line.value })
        elif line.name == 'TEL':
            if ('_PHONES' not in values):
                values['_PHONES'] = [ ]
            telephone = { }
            if ('X-COILS-TEL-TYPE' in line.params):
                telephone['type'] = line.params['X-COILS-TEL-TYPE'][0]
            elif ('TYPE' in line.params):
                telephone['type'] = line.params['TYPE'][0]
            else:
                raise CoilsException('Cannot parse vCard; telephone with no type')
            telephone['number'] = line.value
            values['_PHONES'].append(telephone)
        elif line.name == 'N':
            values['lastName'] = line.value.family
            values['firstName'] = line.value.given
            # Also contains: additional, prefix, suffix
        elif line.name == 'NICKNAME':
            values['descripion'] = line.value
        elif line.name == 'X-EVOLUTION-FILE-AS':
            values['fileAs'] = line.value
        elif line.name == 'X-EVOLUTION-MANAGER':
            # TODO: Implement, bossName
            pass
        elif line.name == 'X-EVOLUTION-ASSISTANT':
            values['assistantName'] = line.value
        elif line.name == 'X-EVOLUTION-SPOUSE':
            # TODO: Implement, spouseName
            pass
        elif line.name == 'X-EVOLUTION-ANNIVERSARY':
            # TODO: Implement, anniversary
            pass
        elif line.name == 'ROLE':
            values['occupation'] = line.value
            pass
        elif line.name == 'BDAY':
            # TODO: Implement
            pass
        elif line.name == 'CALURL':
            # TODO: Implement
            pass
        elif line.name == 'FBURL':
            values['comment'] = line.value
        elif line.name == 'NOTE':
            # TODO: Implement, comment
            pass
        elif line.name == 'CATEGORIES':
            # TODO: Implement, keywords
            pass
        elif line.name == 'CLASS':
            # TODO: Implement, sensistivity
            pass
        elif line.name == 'EMAIL':
            if ('INTERNET' in line.params['TYPE']):
                if ('PREF' in line.params['TYPE']):
                    emails.insert(0, line.value)
                else:
                    emails.append(line.value)
            pass
        elif line.name == 'FN':
            pass
        elif line.name[:22] == 'X-COILS-COMPANY-VALUE-':
            attribute = line.name[22:].lower().replace('-', '_')
            if (len(attribute) > 0):
                if '_COMPANYVALUES' not in values:
                    values['_COMPANYVALUES'] = [ ]
                values['_COMPANYVALUES'].append({'attribute': attribute,
                                                 'value':     line.value})
            pass
        else:
            print 'unprocessed vcard attribute {0}'.format(line.name)
    if ('objectId' not in values):
        pass
    if (len(emails) > 0):
        if '_COMPANYVALUES' not in values:
            values['_COMPANYVALUES'] = [ ]
        count = 1
        for email in emails:
            values['_COMPANYVALUES'].append({'attribute': 'email{0}'.format(count),
                                             'value':     email })
            count = count + 1
    return values

