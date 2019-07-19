from zmqpc import Events

def test_initialization_single():
    e = Events()
    e.close()

# def test_initialization_multiple():
#     l = []
#     for i in range(0, 100):
#         e = Events()
#         l.append(e)
#
#     for e in l:
#         e.close()
