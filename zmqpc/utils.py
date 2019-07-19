def bytes_to_str(a):
    if isinstance(a, bytes):
        a = a.decode('utf-8')
    return a

def str_to_bytes(a):
    if isinstance(a, int):
        a = str(a)
    if isinstance(a, str):
        a = bytes(a, 'utf-8')
    return a
