from multiprocessing.connection import Listener

address = ('localhost', 6000)     # family is deduced to be 'AF_INET'
listener = Listener(address, authkey=b'secret password')
conn = listener.accept()
print("connection accepted from %s:%s" % listener.last_accepted)
while True:
    ret = conn.poll()
    import pdb
    pdb.set_trace()
    if ret:
        msg = conn.recv()
        print(msg)
        # do something with msg
        if msg != 'close':
            conn.close()
            break
listener.close()
