import math

from USocket import UnreliableSocket
from Segment import segment
from SlidingWindow import SendingWindow, ReceiveWindow
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
        self.seqNum = 0  # 表示下一个要发的包的信号
        self.connectAddr = None  # 表示与这个socket相连的ip地址
        self.windowsize = 10  # 表示windowsize的大小 值可在调试过程中修改
        self.isConnected = False
        self.rdt_time = 1
        self.status = []  # 说明当前状态的链表(之所以选链表是因为担心会不止一个状态)
        self.pktTime = {}  # 获取发包的时间戳
        self.RTT = 0  # 获取首发包共使用的时间，用来进行拥塞控制
        # 计算公式 RTT = (1 - rttRate) * RTT + rttRate * SampleRTT
        self.lastSegment = 0

        self.rttRate = 0.125  # 计算rtt时间的比率
        #############################################################################
        #                             END OF YOUR CODE                              #
        #############################################################################

    def reset(self):
        """
        将socket的状态还原
        """
        self.recvSin = False
        self.ackNum = 0
        self.connectAddr = None
        self.isConnected = False
        self.lastSegment = 0

        self.status = []

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
            print("----- Server start listening -------")
            data_client, addr_client = self.recvfrom(1024)
            print("----- Server received -------")
            data = data_client
            data_client = segment.parse(data_client)  # 将受到的数据解码
            if data_client.sin == 1:  # 收到连接请求
                conn.recvSin = True
                conn.ackNum = data_client.seqNumber + 1
                # print("accept:receive connection request!")
                conn.sendto(segment(sin=1, ack=1, ackNumber=conn.ackNum).getSegment(), addr_client)  # 发sin ack
                # print("accept:send sin ack")
                while True:
                    data_client2, addr_client2 = conn.recvfrom(1024)
                    data_client2 = segment.parse(data_client2)
                    # if data_client2.sin == 1 and data_client2.ack == 1 and addr_client2 == addr_client and data_client2.seqNumber == self.ackNum:  # 收到了原来的地址发来的正确报文
                    if data_client2.ack == 1 and data_client2.seqNumber == conn.ackNum and addr_client2 == addr_client:  # 收到了原来的地址发来的正确报文
                        conn.connectAddr = addr_client  # 建立连接
                        conn.isConnected = True
                        print("accept:connection established")
                        conn.status.append('connect')
                        self.reset()  # 重置socket
                        break
                break
        return conn, addr_client
        #############################################################################
        #                             END OF YOUR CODE                              #
        #############################################################################
        return conn, addr

    def connect(self, address: (str, int)):  # client端 ，主动初始化TCP服务器连接，一般address的格式为元组（hostname,
        # port），如果连接出错，返回socket.error错误。
        """
        Connect to a remote socket at address.
        Corresponds to the process of establishing a connection on the client side.
        """
        #############################################################################
        # TODO: YOUR CODE HERE                                                      #
        #############################################################################
        self.connectAddr = address
        self.sendto(segment(sin=1).getSegment(), self.connectAddr)  # 发送请求连接报文
        # print("send connect request")
        data_sever, addr_sever = self.recvfrom(1024)
        # print("receive reply!")
        data_sever = segment.parse(data_sever)
        if data_sever.ack == 1 and data_sever.sin == 1:  # and addr_sever == self.connectAddr:
            self.connectAddr = addr_sever
            # print("received ack")
            self.seqNum = 1
            self.ackNum = data_sever.seqNumber + 1
            self.sendto(segment(ack=1, seqNumber=self.seqNum, ackNumber=self.ackNum).getSegment(),
                        self.connectAddr)
            # print("send ack")
            self.status.append('connect')
            self.isConnected = True

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
        data = b''
        # assert self._recv_from, "Connection not established yet. Use recvfrom instead."
        #############################################################################
        # TODO: YOUR CODE HERE                                                      #
        #############################################################################
        rw = ReceiveWindow(windowSize=50, windowBase=0)  # TODO 估计得改
        while self.isConnected:
            data_sever, addr_sever = self.recvfrom(bufsize)
            data_sever = segment.parse(data_sever)
            print("recv:pkt", data_sever.seqNumber)
            if data_sever.Checksum(data_sever):  # 若收到报文的checksum正确

                if rw.addSegment(seqNum=data_sever.seqNumber, segment=data_sever):  # 若报文正确添加进buffer中，回一个ack
                    # print('recv: add segment successfully')
                    self.sendto(segment(ackNumber=data_sever.seqNumber).getSegment(), self.connectAddr)
                    print('recv: send ack', data_sever.seqNumber)
                elif rw.hasSegment(data_sever.seqNumber) or rw.checkFinish(data_sever.seqNumber):
                    self.sendto(segment(ackNumber=data_sever.seqNumber).getSegment(), self.connectAddr)
            else:
                print('\033[1;45m recv: have wrong data \033[0m')
            while rw.needCheck():
                data = data + rw.checkBuffer().payload
            if data_sever.rst == 1 and data_sever.Checksum(data_sever):
                self.lastSegment = data_sever.seqNumber
            if rw.checkFinish(self.lastSegment) and self.lastSegment != 0:
                print('recv: received all segments')
                break

        #############################################################################
        #                             END OF YOUR CODE                              #
        #############################################################################
        print(str(data))
        return data

    def sender_time_out(self, *args):
        # print('rdt_sender_time_out: time out!')
        # time.sleep(self.RTT)
        self.sendto(args[0].getSegment(), self.connectAddr)
        self.pktTime[args[0].seqNumber] = time.time()
        pass

    def send(self, byte: bytes):  # 发送TCP数据，将string中的数据发送到连接的套接字。返回值是要发送的字节数量，该数量可能小于string的字节大小。
        """
        Send data to the socket.
        The socket must be connected to a remote socket, i.e. self._send_to must not be none.
        """
        # assert self._send_to, "Connection not established yet. Use sendto instead."
        #############################################################################
        # TODO: YOUR CODE HERE                                                      #
        #############################################################################
        if self.isConnected:
            self.pktTime.clear()  # 初始化发包时间
            pieces_size = 100
            datas = self.slice_into_pieces(byte, pieces_size)  # 将包切片
            sw = SendingWindow(window_size=20, datas=datas, sender_time_out_method=self.sender_time_out)  # 初始化发送窗口
            ack_finish = False
            for seq, seg in sw.buffer.items():  # 将窗口内的包发送
                # print("send:send", seg.seqNumber)
                # time.sleep(self.RTT)
                self.sendto(seg.getSegment(), self.connectAddr)
                self.pktTime[seq] = time.time()

            while ack_finish is False:  # 开始发送

                buffer, addr = self.recvfrom(1024)  # 接受ack信息

                # head = buffer[:18]
                seg = segment.parse(buffer)

                if segment.Checksum(seg) is False:
                    continue

                if seg.ackNumber in sw.buffer.keys():

                    con = sw.ack(seg.ackNumber)  # 通知发送窗口接收到了包并且返回结果
                    error = time.time() - self.pktTime[seg.ackNumber]
                    self.RTT = self.RTT + (1 - self.rttRate) + self.rttRate * error
                    print("recieve ack:", seg.ackNumber, "send:self.RTT=", self.RTT)
                    sw.time_out = self.RTT
                    if type(con) == list:  # 返回结果:链表,链表中是滑动窗口后新加入的包,将其一一发送
                        # print('sender: start to slide send window')
                        for segg in con:
                            # TODO:ADD TIME OUT
                            # time.sleep(self.RTT)
                            print("send:send", segg.seqNumber)
                            self.sendto(segg.getSegment(), self.connectAddr)
                            self.pktTime[segg.seqNumber] = time.time()

                    elif con:  # 返回结果:真,说明发送完毕
                        ack_finish = True
                        # print('sender: send finish')

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
        self.sendto(segment(fin=1).getSegment(), self.connectAddr)
        print('fin has been send')
        print('---------closed------------')
        # # initiative close
        # if 'client' in self.status:
        #     self._send_to(segment(fin=1).getSegment())
        #     self._recv_from(1024)
        #     self._recv_from(1024)
        #     self._send_to(segment(ack=1).getSegment())
        # # passivity close
        # else:
        #     # TODO: passivity close
        #     pass
        #############################################################################
        #                             END OF YOUR CODE                              #
        #############################################################################
        super().close()

    def set_send_to(self, send_to):
        self._send_to = send_to

    def set_recv_from(self, recv_from):
        self._recv_from = recv_from

    def slice_into_pieces(self, data: bytes, pieces_size):
        pieces = []
        cnt = math.ceil(len(data) / pieces_size)
        for i in range(0, cnt + 1):
            # 最后一个包rst设为1，代表包发送完毕
            header = segment(rst=1 if i == cnt else 0, seqNumber=i, ackNumber=self.ackNum,
                             payload=data[pieces_size * i:min(pieces_size * (i + 1), len(data))])

            pieces.append(header)

        return pieces


"""
You can define additional functions and classes to do thing such as packing/unpacking packets, or threading.

"""
