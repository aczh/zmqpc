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

    pub.close()
    sub.close()
    time.sleep(0.1)

    return fn.data

def test_str():
    data = 'A廋傗𡙶Ş#踘拯RݜC􎉙򁆰Ὓ姙򝌦F򥆤V愷򎠢򝧿󤮮0Θ񤕪𕖂̪㉎񹈤'
    assert data == simple_recv(data=data)

def test_int():
    data = 26123
    assert data == simple_recv(data=data)

def test_dict():
    data = {'a': 'b', 'c': {'d': 'e'}}
    assert data == simple_recv(data=data)

def test_list():
    data = ['a', 'b', 1, 2, b'5']
    assert data == simple_recv(data=data)
