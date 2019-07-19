import zmq
from threading import Thread

from . constants import DELIMETER

from logging import getLogger
LOG = getLogger(__name__)


class Subscriber:
    '''Simple ZMQ subscriber.'''
    def __init__(self, address='127.0.0.1', timeout=100, callback=None):
        self.address = address
        self.socket = zmq.Context().socket(zmq.SUB)
        self.socket.setsockopt(zmq.RCVTIMEO, timeout)

        self.subscriptions = set()
        self.connections = set()

        # function to be called upon receiving a message
        self.callback = callback

        # listener thread
        self.listening = True
        self.listener = None
        self.start_listening()

    ########################################
    # subscription/connection methods
    ########################################
    def subscribe(self, topic=''):
        if topic not in self.subscriptions:
            self.subscriptions.add(topic)
            self.socket.setsockopt_string(zmq.SUBSCRIBE, topic)
            LOG.debug(f"Socket subscribing to '{topic}'")

    def unsubscribe(self, topic=''):
        if topic in self.subscriptions:
            self.subscriptions.remove(topic)
            self.socket.setsockopt_string(zmq.UNSUBSCRIBE, topic)
            LOG.debug(f"Socket unsubscribing to '{topic}'")

    def connect(self, port):
        if port not in self.connections:
            self.socket.connect(f'tcp://{self.address}:{port}')
            self.connections.add(port)
            LOG.debug(f"Subscriber connecting at {port}")

    def disconnect(self, port):
        if port in self.connections:
            self.socket.disconnect(f'tcp://{self.address}:{port}')
            self.connections.remove(port)
            LOG.debug(f"Subscriber disconnecting at {port}")

    ########################################
    # socket polling
    ########################################
    def start_listening(self):
        self.listening = True
        self.listener = Thread(target=self.listen)
        self.listener.daemon = True
        self.listener.start()

    def listen(self):
        while self.listening:
            try:
                msg = self.socket.recv()
                topic, payload = msg.split(DELIMETER, 1)
                if self.callback:
                    self.callback(topic, payload)
            except zmq.error.Again:
                pass

    ########################################
    # cleanup
    ########################################
    def close(self):
        self.listening = False
        self.listener.join(1)
        if self.socket:
            self.socket.close()
            self.socket = None
