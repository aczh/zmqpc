from zmqpc import Events

from utils import simple_recv

def test_str():
    data = 'A廋傗𡙶Ş#踘拯RݜC􎉙򁆰Ὓ姙򝌦F򥆤V愷򎠢򝧿󤮮0Θ񤕪𕖂̪㉎񹈤'
    recv_data = simple_recv(data=data)
    assert data == recv_data
