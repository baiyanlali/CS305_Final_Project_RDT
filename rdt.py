from USocket import UnreliableSocket
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
        self.segment = None
        self.port = None
        self.dstIP = None
        self.timeout = None
        #############################################################################

        #############################################################################
        #                             END OF YOUR CODE                              #
        #############################################################################

    def accept(self) -> ('RDTSocket', (str, int)):  # 被动接受TCP客户端连接,非阻塞式等待连接的到来
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

        #############################################################################
        #                             END OF YOUR CODE                              #
        #############################################################################
        return conn, addr

    def connect(self, address: (str, int)):  # 主动初始化TCP服务器连接，。一般address的格式为元组（hostname,port），如果连接出错，返回socket.error错误。
        """
        Connect to a remote socket at address.
        Corresponds to the process of establishing a connection on the client side.
        """
        #############################################################################
        # TODO: YOUR CODE HERE                                                      #
        #############################################################################
        raise NotImplementedError()
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

    def recvfrom(self, bufsize) -> bytes:
        pass

    def settimeout(self, value):
        pass

    def send(self, bytes: bytes):  # 发送TCP数据，将string中的数据发送到连接的套接字。返回值是要发送的字节数量，该数量可能小于string的字节大小。
        """
        Send data to the socket.
        The socket must be connected to a remote socket, i.e. self._send_to must not be none.
        """
        assert self._send_to, "Connection not established yet. Use sendto instead."
        #############################################################################
        # TODO: YOUR CODE HERE                                                      #
        #############################################################################
        raise NotImplementedError()
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


class segment:  # 定义传输报文的格式
    """
    [0] sin,fin,ack,rst 1bit,建立连接请求标志,1代表请求建立连接;1bit,结束连接请求标志，1代表请求结束连接;1bit,1表示收到请求，包括sin和fin;rst为1bit，表示请求重新建立连接
    [1:4] seqNumber 32bit,表示将要发出的包的序号
    [5:8] ackNumber  32bit，表示想要收到的包的序号
    [9:12] Length  32bit,表示payload的长度，单位byte，不包括报文头
    [13:14] checksum 16bit,校验和
    """

    def __init__(self):  # 初始化报文
        self.sin = 0
        self.fin = 0
        self.ack = 0
        self.rst = 0

        self.seqNumber = 0
        self.ackNumber = 0

        self.length = 0
        self.checksum = 0

        self.payload = ''

    def getLength(self):  # 求payload的长度
        self.length = len(self.payload)

    def getFlag(self) -> bytes:  # 将sin，fin,ack,rst打包成一个byte
        s = str(self.sin) + str(self.fin) + str(self.ack) + str(self.rst) + "0000"
        return s.encode()

    def getChecksum(self):  # 求checksum
        s = self.payload.encode()
        checksum = 0
        for i in s:
            checksum += i
        checksum = checksum % 4294967296
        self.checksum = checksum

    def payloadToByte(self) -> bytes:  # 将payload转换成bytes
        s = self.payload
        return s.encode()

    def getSegment(self) -> bytes:  # 将整个报文转换为bytes
        byte = self.getFlag() + self.seqNumber.to_bytes(4, 'big') + self.ackNumber.to_bytes(4,
                                                                                            'big') + self.length.to_bytes(
            4, 'big') + self.checksum.to_bytes(2, 'big') + self.payloadToByte()
