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
import sys, logging, os, yaml
from multiprocessing import Pipe
from packet          import Packet
from broker          import Broker

class Service(object):
    __auto_dispatch__ = False
    __is_worker__     = False

    def __init__(self):
        self._shutdown = False

    def setup(self):
        sys.stdin.close()
        self._pid = os.getpid()
        self._broker = Broker()
        self.log = logging.getLogger('{0}[{1}]'.format(self.__service__, os.getpid()))
        self._broker.subscribe(self.__service__, self.receive_message)

    def send(self, packet):
        self.log.debug('Sending {0} to {1}'.format(packet.uuid, packet.target))
        # TODO: Set timeout and deal with Queue.Full exception
        self._broker.send(packet)

    def shutdown(self):
        #print '{0} PID#{1} shutting down.'.format(self.__service__, os.getpid())
        self.log.debug('{0} PID#{1} shutting down.'.format(self.__service__, os.getpid()))
        self.log.debug('Shutting down AMQ broker.')
        #print 'Shutting down AMQ broker'
        self._broker.close()
        sys.stdout.close()
        sys.stderr.close()        
        sys.exit(0)

    def receive_message(self, message):
        packet = self._broker.packet_from_message(message)
        if (packet is not None):
            #print 'received {0} from {1}'.format(packet.uuid, packet.source)
            method    = Packet.Method(packet.target).lower()
            parameter = Packet.Parameter(packet.target)
            response = self.process(method, parameter, packet)
            if (response is not None):
                self.send(response)

    def wait(self, timeout=None):
        self._broker.wait(timeout)

    def prepare(self):
        try:
            import procname
            procname.setprocname('service::{0}'.format(self.__service__))
        except:
            self.log.info('Failed to set process name for service')
        packet = Packet('{0}/__hello_ack'.format(self.__service__),
                        'coils.master/__hello', self.__service__)
        self.hello_uuid = packet.uuid
        self.send(packet)

    def process(self, method, parameter, packet):
        if ((method == '__ping') or (method == '__hello')):
            # From a services point of view a ping and a hello are the same thing.
            return Packet.Reply(packet, packet.data)
        elif (method == '__hello_ack'):
            # A hello ack should be in reply to our hello and have as data
            # the name of ourselves.
            if ((self.hello_uuid == packet.reply_to) and
                (str(packet.data) == self.__service__)):
                self.log.debug('Recevied valid Hello ACK from {0}'.format(packet.source))
            else:
                pass
                #print self.__service__
                #print '  Received invalid Hello ACK (not mine)'
                #print '  Source        :    {0}'.format(packet.source)
                #print '  Target        :    {0} [I am {1}]'.format(packet.target, self.__service__)
                #print '  Expecting UUID:    {0}'.format(self.hello_uuid)
                #print '  Got reply to UUID: {0}'.format(packet.reply_to)
                #raise Exception('Corrupted message bus; Hello ACK not mine.')
        elif (method == '__shutdown'):
                self.shutdown()
        elif (self.__auto_dispatch__):
            method = 'do_{0}'.format(method)
            if (hasattr(self, method)):
                return getattr(self, method)(parameter, packet)
        return None

    def work(self):
        pass

    def run(self):
        self.setup()
        self.prepare()
        while (not self._shutdown):
            if (self.__is_worker__):
                self.wait(timeout=1)
            else:
                self.wait(timeout=10)
            if (self.__is_worker__):
                self.work()



