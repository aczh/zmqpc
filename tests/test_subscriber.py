from zmqpc.subscriber import Subscriber

def test_initialization():
    for i in range(0, 50):
        s = Subscriber()
        s.close()


def test_subscribe():
    s = Subscriber()
    s.subscribe('񣻠Ұ槝㦛숱پ󱌏㡡􊐜󐴠ἻЦӜÛ𡫚s㕓<ǉeQԨ!S􃴛OᢍمH&Ɛ㉟')
    s.close()
