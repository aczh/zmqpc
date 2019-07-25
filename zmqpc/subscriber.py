import zmq
import uuid
from threading import Thread

from . constants import DELIMETER
from . publisher import Publisher
from . utils import str_to_bytes, bytes_to_str

from logging import getLogger
LOG = getLogger(__name__)


class SubscriberRequests:
    SUB_ADD = b'1'
    SUB_REMOVE = b'2'
    CONN_ADD = b'3'
    CONN_REMOVE = b'4'

class Subscriber:
    '''
    ZMQ Subscriber.
    Can subscribe/unsubscribe from topics.
    Can connect/disconnect from IPs.

    ZMQ is not thread-safe.
    To get around this, we use a publisher req_socket to publish events to the main subscriber socket.
    The subscriber socket is created in a seperate thread.
    It connects/subscribes to the req_socket's port and special subscription topic.
    It connects/disconnects and subscribes/unsubscribes baseed on events from the req_socket.
    '''
    def __init__(self, address='127.0.0.1', timeout=100, callback=None):
        self.address = address
        self.timeout = timeout

        # function to be called upon receiving a message
        self.callback = callback

        # listener thread
        self.listening = True
        self.listener = None

        # socket that sends subscribe/unsubscribe and connect/disconnet messages to listener socket.
        self.req_socket = Publisher()
        self.req_topic = str(uuid.uuid4())
        self.req_topic_bytes = str_to_bytes(self.req_topic)

        self.listener_ready = False
        self.queued_listener_funcs = []

        self.start_listening()

    ########################################
    # subscription/connection methods
    ########################################
    def listener_is_ready(self):
        self.listener_ready = True
        for publish_data in self.queued_listener_funcs:
            self.req_socket.publish(self.req_topic, publish_data)
        print("LISTENER IS READY")

    def subscribe(self, topic=''):
        publish_data = SubscriberRequests.SUB_ADD + str_to_bytes(topic)
        if not self.listener_ready:
            self.queued_listener_funcs.append(publish_data)
        else:
            self.req_socket.publish(self.req_topic, publish_data)
        LOG.debug(f'Subscriber {self.req_socket.port} requesting subscription to topic: {topic}')

    def unsubscribe(self, topic=''):
        publish_data = SubscriberRequests.SUB_REMOVE + str_to_bytes(topic)
        if not self.listener_ready:
            self.queued_listener_funcs.append(publish_data)
        else:
            self.req_socket.publish(self.req_topic, publish_data)

        LOG.debug(f'Subscriber {self.req_socket.port} requesting unsubscription from topic: {topic}')

    def connect(self, port):
        publish_data = SubscriberRequests.CONN_ADD + str_to_bytes(f'tcp://{self.address}:{port}')
        if not self.listener_ready:
            self.queued_listener_funcs.append(publish_data)
        else:
            self.req_socket.publish(self.req_topic, publish_data)
        LOG.debug(f'Subscriber {self.req_socket.port} requesting connection to topic: {port}')

    def disconnect(self, port):
        publish_data = SubscriberRequests.CONN_REMOVE + str_to_bytes(f'tcp://{self.address}:{port}')
        if not self.listener_ready:
            self.queued_listener_funcs.append(publish_data)
        else:
            self.req_socket.publish(self.req_topic, publish_data)
        LOG.debug(f'Subscriber {self.req_socket.port} requesting disconnection from topic: {port}')

    ########################################
    # socket polling
    ########################################
    def start_listening(self):
        self.listening = True
        self.listener = Thread(target=self.listen)
        self.listener.daemon = True
        self.listener.start()

    def listen(self):
        '''
        Function that creates a socket that listens on loop.
        Designed to be run on a seperate thread.
        The socket created in this thread should NOT be used outside of this thread.
        '''
        # initialize the socket
        socket = zmq.Context().socket(zmq.SUB)
        socket.setsockopt(zmq.RCVTIMEO, self.timeout)

        # connect the socket to our requester socket
        socket.connect(f'tcp://{self.address}:{self.req_socket.port}')
        socket.setsockopt_string(zmq.SUBSCRIBE, self.req_topic)

        self.listener_is_ready()

        while self.listening:
            try:
                msg = socket.recv()
                topic, payload = msg.split(DELIMETER, 1)
                if topic == self.req_topic_bytes:
                    # this message came from our requester socket.
                    req = payload[0:1]
                    req_data = bytes_to_str(payload[1:])
                    if req == SubscriberRequests.SUB_ADD:
                        socket.setsockopt_string(zmq.SUBSCRIBE, req_data)
                        LOG.debug(f'Subscriber {self.req_socket.port} subscribed to topic: {req_data}')
                    elif req == SubscriberRequests.SUB_REMOVE:
                        socket.setsockopt_string(zmq.UNSUBSCRIBE, req_data)
                        LOG.debug(f'Subscriber {self.req_socket.port} unsubscribed from topic: {req_data}')
                    elif req == SubscriberRequests.CONN_ADD:
                        socket.connect(req_data)
                        LOG.debug(f'Subscriber {self.req_socket.port} connected to port: {req_data}')
                    elif req == SubscriberRequests.CONN_REMOVE:
                        socket.disconnect(req_data)
                        LOG.debug(f'Subscriber {self.req_socket.port} disconnected from port: {req_data}')
                elif self.callback:
                    self.callback(topic, payload)
            except zmq.error.Again:
                pass

        socket.close()

    ########################################
    # cleanup
    ########################################
    def close(self):
        self.listening = False
