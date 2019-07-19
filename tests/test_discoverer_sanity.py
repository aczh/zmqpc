from zmqpc.discoverer import Discoverer

def test_initialization_single():
    d = Discoverer('id')
    d.close()

# def test_initialization_multiple():
#     for i in range(0, 100):
#         p = Publisher()
#         p.close()
#
# def test_sanity_publish():
#     p = Publisher()
#     p.publish(
#         '7Jɨ񷍯ݪ򃧀򰧋񉰜檜ɏɀ.kC𔌀ê󵖪󀤈V򫋣񄑗omkpYWF*أל',
#         rb'\xa8(\xe8vlD\x0c\xe53q@L\x15\x10\xb2I&Z_\xd6:U\xf4-'
#     )
#     p.close()
