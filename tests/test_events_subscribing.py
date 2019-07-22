import uuid
import time
from zmqpc import Events

def test_subscribe_multiple():
    pub = Events()
    sub = Events()

    time.sleep(0.1)

    # set up subscriber connection
    def fn(data):
        fn.data = data
        fn.calls += 1
    fn.data = None
    fn.calls = 0

    topics = []
    for i in range(0, 100):
        topics.append(str(i))

    for topic in topics:
        sub.connect(fn, topic)

    for topic in topics:
        pub.publish(topic, topic)

    time.sleep(0.1)

    pub.close()
    sub.close()

    assert fn.calls == len(topics)
