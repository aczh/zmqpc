from zmqpc import Events

from utils import simple_recv

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
