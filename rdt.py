from USocket import UnreliableSocket
from Segment import segment
import threading
import time


class RDTSocket(UnreliableSocket):
    """
    The functions with which you are to build your RDT.
    -   recvfrom(bufsize)->bytes, addr
    -   sendto(bytes, address)
    -   bind(address)

    You can set the mode of the socket.
    -   settimeout(timeout)
    -   setblocking(flag)
    By default, a socket is created in the blocking mode.
    https://docs.python.org/3/library/socket.html#socket-timeouts

    """

    def __init__(self, rate=None, debug=True):  # 建立一个新的socket时，所需初始化的状态,程序中使用的新变量记得在此初始化
        super().__init__(rate=rate)
        self._rate = rate
        self._send_to = None
        self._recv_from = None
        self.debug = debug
        #############################################################################
        # TODO: ADD YOUR NECESSARY ATTRIBUTES HERE
        #############################################################################
        self.recvSin = False  # 表示是否收到建立连接的请求
        self.ackNum = 0  # 表示下一个想要的包的信号
        self.connectAddr = None  # 表示与这个socket相连的ip地址
        self.recvSin = False  # 表示是否收到建立连接的请求
        self.ackNum = 0  # 表示下一个想要的包的信号

        self.IPdst = ''  # 建立连接后终点IP地址
        self.status = []  # 说明当前状态的链表(之所以选链表是因为担心会不止一个状态)
        #############################################################################
        #                             END OF YOUR CODE                              #
        #############################################################################

    def accept(self) -> ('RDTSocket', (str, int)):  # sever端，被动接受client端连接,非阻塞式等待连接的到来
        """
        Accept a connection. The socket must be bound to an address and listening for
        connections. The return value is a pair (conn, address) where conn is a new
        socket object usable to send and receive data on the connection, and address
        is the address bound to the socket on the other end of the connection.

        This function should be blocking.
        """
        conn, addr = RDTSocket(self._rate), None
        #############################################################################
        # TODO: YOUR CODE HERE                                                      #
        #############################################################################
        while True:
            data_client, addr_client = self.recvfrom(1024)
            data_client = segment.parse(data_client)  # 将受到的数据解码
            if data_client.syn == 1:
                self.recvSin = True
                self.ackNum = data_client.seqNumber + 1
            conn.sendto(segment(sin=1, ack=1, ackNumber=self.ackNum).getSegment(), addr_client)
            while True:
                data_client2, addr_client2 = self.recvfrom(1024)
                data_client2 = segment.parse(data_client2)
                if data_client2.syn == 1 and data_client2.ack == 1 and addr_client2 == addr_client and data_client2.seqNumber == self.ackNum:
                    conn.connectAddr = addr_client
                    conn.sendto(segment(ack=1, ackNumber=data_client2.seqNumber + 1).getSegment(), addr_client)
                    self.__init__()
                    break
            break
        return conn, addr_client
        #############################################################################
        #                             END OF YOUR CODE                              #
        #############################################################################
        return conn, addr

    def connect(self, address: (str, int)):  # client端 ，主动初始化TCP服务器连接，一般address的格式为元组（hostname,port），如果连接出错，返回socket.error错误。
        """
        Connect to a remote socket at address.
        Corresponds to the process of establishing a connection on the client side.
        """
        #############################################################################
        # TODO: YOUR CODE HERE                                                      #
        #############################################################################
        
        self._send_to(segment(sin=1).getSegment())
        self._recv_from(1024)
        #############################################################################
        #                             END OF YOUR CODE                              #
        #############################################################################

    def recv(self, bufsize: int) -> bytes:  # 接收TCP数据，数据以字符串形式返回，bufsize指定要接收的最大数据量。flag提供有关消息的其他信息，通常可以忽略。
        """
        Receive data from the socket.
        The return value is a bytes object representing the data received.
        The maximum amount of data to be received at once is specified by bufsize.

        Note that ONLY data send by the peer should be accepted.
        In other words, if someone else sends data to you from another address,
        it MUST NOT affect the data returned by this function.
        """
        data = None
        assert self._recv_from, "Connection not established yet. Use recvfrom instead."
        #############################################################################
        # TODO: YOUR CODE HERE                                                      #
        #############################################################################

        #############################################################################
        #                             END OF YOUR CODE                              #
        #############################################################################
        return data

    def send(self, bytes: bytes):  # 发送TCP数据，将string中的数据发送到连接的套接字。返回值是要发送的字节数量，该数量可能小于string的字节大小。
        """
        Send data to the socket.
        The socket must be connected to a remote socket, i.e. self._send_to must not be none.
        """
        assert self._send_to, "Connection not established yet. Use sendto instead."
        #############################################################################
        # TODO: YOUR CODE HERE                                                      #
        #############################################################################
        if 'connect' in self.status:
            seqNumber=0
            pieces=1000
            segment(seqNumber=seqNumber,)
            segment()
            self.status.remove('connect')
            self.sendto(bytes, self.IPdst)
        #############################################################################
        #                             END OF YOUR CODE                              #
        #############################################################################

    def close(self):  # 关闭套接字
        """
        Finish the connection and release resources. For simplicity, assume that
        after a socket is closed, neither futher sends nor receives are allowed.
        """
        #############################################################################
        # TODO: YOUR CODE HERE                                                      #
        #############################################################################
        # initiative close
        self._send_to(segment(fin=1).getSegment())
        self._recv_from(1024)
        self._recv_from(1024)
        self._send_to(segment(ack=1).getSegment())
        # passivity close

        #############################################################################
        #                             END OF YOUR CODE                              #
        #############################################################################
        super().close()

    def set_send_to(self, send_to):
        self._send_to = send_to

    def set_recv_from(self, recv_from):
        self._recv_from = recv_from


"""
You can define additional functions and classes to do thing such as packing/unpacking packets, or threading.

"""



