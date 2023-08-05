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
import os, sys, glob, inspect, time, logging
try:
  from coils.foundation import *
except ImportError:
  print 'Coils Model package not found, required by Coils Core!'
  sys.exit(2)
from entityaccessmanager import EntityAccessManager
from bundlemanager       import BundleManager

class AccessManager:

    def __init__(self):
        self.log = logging.getLogger('accessmanager')

    def filter_by_access(self, ctx, rights, entities, **params):
        result = [ ]
        if ( not ( isinstance(entities, list) ) ):
            entities = [ entities ]
        start = time.time()
        # The "one_kind_hack" param lets us avoid calling the TypeManager,
        # which saves time [potentially a lot of time].  The caller can
        # specify this when it knows for certain all the objects in the
        # collection are of the specified type. The value of the one_kind_hack
        # parameter must be a valid case-sensitive entity name, like "Contact"
        if (params.has_key('one_kind_hack')):
            objects = { params['one_kind_hack']: entities }
        else:
            objects = ctx.type_manager().group_by_type(objects=entities)
        for kind in objects.keys():
            manager = BundleManager.get_access_manager(kind, ctx)
            self.log.debug('filtering %s using %s' % (kind, repr(manager)))
            x = manager.materialize_rights(objects=objects[kind])
            start_filter = time.time()
            for k in x.keys():
                if (set(list(rights.lower())).issubset(x[k])):
                    result.append(k)
            end_filter = time.time()
            self.log.debug('%s: duration of filter for %s was %0.3fs' % (
                repr(self),
                kind,
                (end_filter - start_filter)))
        self.log.debug('access filter returning %d of %d objects' % (len(result), len(entities)))
        end = time.time()
        self.log.debug('%s: duration of filter_by_access was %0.3fs' % (repr(self), (end - start)))
        return result

    def access_rights(self, entity):
        result = { }
        manager = BundleManager.get_access_manager(kind, ctx)
        x = manager.materialize_rights(objects=[entity])
        return x[entity]