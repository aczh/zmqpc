import atexit
import pyarrow
import inspect

from . publisher import Publisher
from . subscriber import Subscriber
from . discoverer import Discoverer
from . utils import bytes_to_str

class Events:
    def __init__(self):
        self.p = Publisher()
        self.s = Subscriber(callback=self.on_message)
        self.d = Discoverer(id=self.p.port, callback=self.on_port_discovery)

        self.topic_to_fn = {}

        atexit.register(self.close)

    def on_port_discovery(self, port):
        self.s.connect(port)

    def on_message(self, topic, payload):
        topic = bytes_to_str(topic)
        if topic in self.topic_to_fn:
            args, kwargs = self.deserialize(payload)

            to_call = self.topic_to_fn[topic]
            to_call_spec = inspect.getfullargspec(to_call)

            to_call_kwargs_num = 0 if to_call_spec.defaults is None else len(to_call_spec.defaults)
            to_call_args_num = len(to_call_spec.args) - to_call_kwargs_num

            # prune out extra args
            if to_call_spec.varargs == None and len(args) > to_call_args_num:
                args = args[:to_call_args_num]

            # prune out extra kwargs
            if to_call_spec.varkw == None and len(kwargs) > to_call_kwargs_num:
                kwargs = {k:v for k, v in kwargs.items() if k in to_call_spec.args[-to_call_kwargs_num:]}

            to_call(*args, **kwargs)

    def connect(self, receiver, topic):
        topic = bytes_to_str(topic)
        self.s.subscribe(topic)
        self.topic_to_fn[topic] = receiver

    def publish(self, topic, *args, **kwargs):
        serialized = self.serialize((args, kwargs))
        self.p.publish(topic, serialized)

    def serialize(self, obj):
        return pyarrow.serialize(obj).to_buffer().to_pybytes()

    def deserialize(self, obj):
        return pyarrow.deserialize(obj)

    def close(self):
        self.p.close()
        self.s.close()
        self.d.close()
