import zmq
from logging import getLogger

from . constants import DELIMETER
from . utils import str_to_bytes

LOG = getLogger(__name__)


class Publisher:
    '''Simple ZMQ publisher.'''

    def __init__(self, address='127.0.0.1', port=None):
        self.socket = zmq.Context().socket(zmq.PUB)
        self.address = address
        self.port = port
        # dynamic port binding if no port is specified
        if port is None:
            self.port = self.socket.bind_to_random_port(f"tcp://{self.address}")
        else:
            self.socket.bind(f'tcp://{self.address}:{self.port}')
        LOG.debug(f'ZMQ Publisher binding to {self.port}')

    def publish(self, topic, data):
        topic = str_to_bytes(topic)
        bstring = topic + DELIMETER + data
        self.socket.send(bstring)

    def close(self):
        if self.socket:
            self.socket.close()
            self.socket = None
