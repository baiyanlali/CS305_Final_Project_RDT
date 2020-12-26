import rdt
if __name__=="__main__":
    socket = rdt.RDTSocket()
    socket.connect(('127.0.0.1',10086))