import rdt

if __name__ == "__main__":
    socket = rdt.RDTSocket()
    socket.bind(('127.0.0.1', 10086))
    sock, addr = socket.accept() # type: (rdt.RDTSocket,(str,int))

    while True:
        sock.send(b'10086,2333')
