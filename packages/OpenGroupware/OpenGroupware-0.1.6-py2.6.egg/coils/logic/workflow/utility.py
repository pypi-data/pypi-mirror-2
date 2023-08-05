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
import datetime
from coils.foundation import *

def filename_for_message_text(uuid):
    return '{0}/wf/m/{1}'.format(Backend.store_root(), str(uuid))

def filename_for_deleted_message_text(uuid):
    return '{0}/wf/m/{1}.deleted'.format(Backend.store_root(), str(uuid))

def filename_for_route_markup(route):
    return '{0}/wf/r/{1}.{2}.bpml'.format(Backend.store_root(),
                                           route.name,
                                           route.version)

def filename_for_deleted_route_markup(route):
    timestamp = datetime.datetime.now().strftime('%s')
    return '{0}/wf/r/{1}.{2}.deleted.bpml'.format(Backend.store_root(),
                                                  route.name,
                                                  timestamp)

def filename_for_process_markup(process):
    return '{0}/wf/p/{1}.bpml'.format(Backend.store_root(),
                                       process.object_id)

def filename_for_deleted_process_markup(process):
    return '{0}/wf/p/{1}.deleted.bpml'.format(Backend.store_root(),
                                               process.object_id)


def filename_for_process_code(process):
    return '{0}/wf/p/{1}.{2}.cpm'.format(Backend.store_root(),
                                          process.object_id,
                                          process.version)


