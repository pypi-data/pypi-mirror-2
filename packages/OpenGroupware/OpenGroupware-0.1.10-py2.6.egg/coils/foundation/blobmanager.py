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
import codecs, os, foundation
from tempfile            import SpooledTemporaryFile
from foundation          import STORE_ROOT


def blob_manager_for_ds(project):
    if (project.url is None):
        return DBFS1Manager()
    driver = project.url.split(':')[0]
    if (driver == 'skyrix'):
        return DBFS1Manager
    elif (driver == 'file'):
        return SkyFSManager
    else:
        raise 'Unknown Data Store driver type of {0}'.format(driver)

class BLOBManager(object):

    __slots__ = ()

    @staticmethod
    def Create(name, encoding='utf-8', version=None):
        filename = u'{0}/{1}'.format(foundation.STORE_ROOT, name)
        if (encoding == 'binary'):
            return open(filename, 'wb')
        else:
            return codecs.open(filename, 'wb', encoding=encoding)

    @staticmethod
    def Open(name, mode, encoding='utf-8', version='0'):
        filename = u'{0}/{1}'.format(foundation.STORE_ROOT, name)
        if (os.path.exists(filename)):
            if (encoding == 'binary'):
                return open(filename, mode)
            else:
                return codecs.open(filename, mode, encoding=encoding)
        return None

    @staticmethod
    def Close(handle):
        if (handle is not None):
            handle.close()

    @staticmethod
    def Delete(name, version='0'):
        filename = u'{0}/{1}'.format(foundation.STORE_ROOT, name)
        if (os.path.exists(filename)):
            os.remove(filename)
            return True
        return False

    @staticmethod
    def ScratchFile(suffix='.data'):
        return SpooledTemporaryFile(max_size=65535,
                                     prefix='Coils.',
                                     suffix=suffix,
                                     dir=u'{0}/tmp'.format(foundation.STORE_ROOT))

    @staticmethod
    def List(name):
        return os.listdir('{0}/{1}'.format(foundation.STORE_ROOT, name))

    @staticmethod
    def SizeOf(name, version='0'):
        return os.path.getsize('{0}/{1}'.format(foundation.STORE_ROOT, name))

    @staticmethod
    def Exists(name, version='0'):
        return os.path.exists('{0}/{1}'.format(foundation.STORE_ROOT, name))
