import time

from zmqpc import Events

def simple_recv(topic='test_topic', data=None):
    pub = Events()
    sub = Events()

    # set up subscriber connection
    def fn(data):
        fn.data = data
    fn.data = None

    time.sleep(0.1)
    sub.connect(fn, topic)

    time.sleep(0.1)
    pub.publish(topic, data)

    time.sleep(0.1)
    return fn.data
