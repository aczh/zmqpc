import os
import time

from zmqpc.discoverer import Discoverer

def test_initialization_single():
    d = Discoverer('id')
    d.close()

def test_initialization_multiple():
    for i in range(0, 50):
        d = Discoverer('id')
        d.close()

def test_discovery():
    ids = set()
    for i in range(0, 50):
        ids.add(os.urandom(10))

    l = []
    for id in ids:
        d = Discoverer(id)
        l.append(d)

    time.sleep(0.1)

    for d in l:
        d.close()

    for d in l:
        assert d.friends.issubset(ids)
