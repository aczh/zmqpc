import sys
import struct
import socket
from threading import Thread
from logging import getLogger

from . constants import MAGIC
from . utils import str_to_bytes

LOG = getLogger(__name__)


class Discoverer:
    '''
    Emulates a SSDP-like discovery protocol on a specified discovery port.
    Each Discoverer has a (preferably unique) ID.
    Upon startup, a Discoverer announces its ID, then begins listening for other announcements.
    Upon hearing an announcement from an ID it does not recognize, it adds the ID to a set and reannounces its own ID.
    '''

    def __init__(self, id, port=50000, callback=None):
        self.id = str_to_bytes(id)
        self.port = port

        # optional function that will be called upon new ID discovery.
        self.callback = callback

        # set that holds previously seen IDs
        self.friends = set()
        self.friends.add(self.id)

        # listener thread
        self.listening = True
        self.listener = Thread(target=self.listen)
        self.listener.daemon = True
        self.listener.start()

    def announce(self):
        '''Broadcasts our ID.'''
        self.socket.sendto(MAGIC + self.id, ('<broadcast>', self.port))
        LOG.debug(f'Discoverer {self.id} announcing.')

    def initialize_socket(self):
        # build a UDP broadcast socket that multiple clients can bind to
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        self.join = False
        try:
            self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        except: pass
        try:
            self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
        except: pass

        if sys.maxsize > 2**32:
            time = struct.pack(str("ll"), int(1), int(0))
        else:
            time = struct.pack(str("ii"), int(1), int(0))
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_RCVTIMEO, time)

        self.socket.bind(('', self.port))

    def listen(self):
        '''
        Listens for broadcasts on a loop.
        Upon hearing a broadcast, check to see if the ID isn't recognized.
        If it isn't, add it to our list of heard IDs, announce ourselves, and call our callback.
        '''
        self.initialize_socket()

        self.announce()

        while self.listening:
            try:
                data, addr = self.socket.recvfrom(1024)
                if not self.listening:
                    break
                if data.startswith(MAGIC):
                    recv_id = data[len(MAGIC):]
                    if recv_id not in self.friends:
                        self.friends.add(recv_id)
                        LOG.debug(f'Discoverer {self.id} found {recv_id}.')
                        if self.callback:
                            self.callback(int(recv_id))
                        self.announce()
            except: pass

        LOG.debug(f'Discoverer {self.id} closed.')

    def close(self):
        self.listening = False
