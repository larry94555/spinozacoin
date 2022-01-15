import asyncio

class Client(asyncio.Protocol):

    def __init__(self):
        #self.log = logging.getLogger('client')
        self.address = None
        self.transport = None

    def connection_made(self, transport):
        self.transport = transport
        self.address = transport.get_extra_info('peername')
        print('{}:{} connected'.format(*self.address))

    def data_received(self, data):
            print('{}:{} just sent {!r}'.format(*self.address, data))

    def eof_received(self):
        print('{}:{} sent EOF'.format(*self.address))

    def connection_lost(self, error=""):
        print('{}:{} disconnected'.format(*self.address))
        self.transport.close()
