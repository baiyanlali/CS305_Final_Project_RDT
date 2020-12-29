from socket import socket, AF_INET, SOCK_DGRAM, inet_aton, inet_ntoa
import random, time
import threading, queue
from socketserver import ThreadingUDPServer
from Segment import segment

lock = threading.Lock()


def bytes_to_addr(bytes):
    return inet_ntoa(bytes[:4]), int.from_bytes(bytes[4:8], 'big')


def addr_to_bytes(addr):
    return inet_aton(addr[0]) + addr[1].to_bytes(4, 'big')


def corrupt(data: bytes) -> bytes:
    raw = list(data)
    e = random.randint(0,1e1)
    for _ in range(0, random.randint(0, 3)):
        if e==0:
            pos = random.randint(0, len(raw) - 1)
            raw[pos] = random.randint(0, 255)

    return bytes(raw)


class Server(ThreadingUDPServer):
    def __init__(self, addr, rate=None, delay=None, corrupt=None):
        super().__init__(addr, None)
        self.rate = rate
        self.buffer = 0
        self.delay = delay
        self.corrupt = corrupt

        self.cnt = 0

    def verify_request(self, request, client_address):
        if self.buffer < 10:
            self.buffer += 1
            return True
        else:
            return False

    def finish_request(self, request, client_address):
        self.cnt = self.cnt + 1
        data, socket = request
        lock.acquire()
        # print(f'network:sleep time {len(data) / self.rate}')
        if self.rate: time.sleep(len(data) / self.rate)
        self.buffer -= 1
        lock.release()

        to = bytes_to_addr(data[:8])
        # print(client_address, to)
        ss = segment.parse(data[8:])
        if self.cnt >= 3:
            data = corrupt(data)
        sss = segment.parse(data[8:])
        if(ss.checksum != sss.checksum):
            print(f'{segment.getChecksum(sss)},{sss.checksum}')
        socket.sendto(addr_to_bytes(client_address) + data[8:], to)


server_address = ('127.0.0.1', 12345)

if __name__ == '__main__':
    with Server(server_address, corrupt=corrupt) as server:
        server.serve_forever()
