class segment:  # 定义传输报文的格式
    """
    [0] sin,fin,ack,rst 1bit,建立连接请求标志,1代表请求建立连接;1bit,结束连接请求标志，1代表请求结束连接;1bit,1表示收到请求，包括sin和fin;rst为1bit，表示请求重新建立连接
    [1:4] seqNumber 32bit,表示将要发出的包的序号,4bytes
    [5:8] ackNumber  32bit，表示想要收到的包的序号,4bytes
    [9:12] Length  32bit,表示payload的长度，单位byte，不包括报文头,4bytes
    [13:14] checksum 16bit,校验和,2bytes
    表头共长为：116bit(4bit+112bit)
    """

    def __init__(self, sin=0, fin=0, ack=0, rst=0, seqNumber=0, ackNumber=0, length=0, checkSum=0,
                 payload: bytes = b''):  # 初始化报文
        self.sin = sin
        self.fin = fin
        self.ack = ack
        self.rst = rst

        self.seqNumber = seqNumber
        self.ackNumber = ackNumber

        # self.checksum = checkSum

        self.payload = payload
        self.length = len(payload)
        self.getChecksum()

    def getLength(self):  # 求payload的长度
        self.length = len(self.payload)

    def getFlag(self) -> bytes:  # 将sin，fin,ack,rst打包成一个byte
        s = str(self.sin) + str(self.fin) + str(self.ack) + str(self.rst)
        return s.encode("UTF-8")
        # return i.to_bytes(1,byteorder='little')

    @staticmethod
    def getFlagStatic(sin=0, fin=0, ack=0, rst=0):
        s = str(sin) + str(fin) + str(ack) + str(rst)
        return s.encode("UTF-8")

    def getChecksum(self) -> int:  # 求checksum
        s = self.getFlag() + self.seqNumber.to_bytes(4, byteorder='little') + \
            self.ackNumber.to_bytes(4, byteorder='little') + \
            self.length.to_bytes(4, byteorder='little') + \
            self.payload #self.payloadToByte()
        check_sum = 0
        for i in s:
            check_sum += i
        checksum = check_sum % 4294967296
        self.checksum = check_sum
        return checksum

    @staticmethod
    def Checksum(seg: 'segment') -> bool:
        s = seg.getFlag() + seg.seqNumber.to_bytes(4, byteorder='little') + \
            seg.ackNumber.to_bytes(4, byteorder='little') + \
            seg.length.to_bytes(4, byteorder='little') +\
            seg.payload
            #+ \
            # seg.payloadToByte()
        checksum = 0
        for i in s:
            checksum += i
        checksum = checksum % 4294967296

        return seg.checksum == checksum

    # def payloadToByte(self) -> bytes:  # 将payload转换成bytes
    #     s = self.payload
    #     return s.encode()
    #
    # @staticmethod
    # def payloadToByteStatic(payload:bytes) -> bytes:  # 将payload转换成bytes
    #     s = payload
    #     return s.encode()

    def __str__(self):
        return self.getFlag() + self.seqNumber.to_bytes() + self.ackNumber.to_bytes() + self.length.to_bytes() + self.checksum.to_bytes() + self.payloadToByte()

    def getSegment(self) -> bytes:  # 将整个报文转换为bytes
        byte = self.getFlag() + self.seqNumber.to_bytes(4, byteorder='little') + \
               self.ackNumber.to_bytes(4, byteorder='little') + \
               self.length.to_bytes(4, byteorder='little') + \
               self.checksum.to_bytes(2, byteorder='little') + self.payload #self.payloadToByte()
        return byte

    @staticmethod
    def getSegmentStatic(sin=0, fin=0, ack=0, rst=0, seqNumber=0, ackNumber=0, length=0, checksum=0,
                         payload=b'') -> bytes:  # 将整个报文转换为bytes
        seqNumberData = seqNumber.to_bytes(4, byteorder='little')
        ackNumberData = ackNumber.to_bytes(4, byteorder='little')
        lengthData = length.to_bytes(4, byteorder='little')
        checksumData = checksum.to_bytes(4, byteorder='little')
        payloadData = payload #segment.payloadToByteStatic(payload)

        byte = segment.getFlagStatic(sin, fin, ack,
                                     rst) + seqNumberData \
               + ackNumberData \
               + lengthData \
               + checksumData \
               + payloadData
        return byte

    @staticmethod
    def parse(data: bytes) -> 'segment':
        sin = data[0] - 48
        fin = data[1] - 48
        ack = data[2] - 48
        rst = data[3] - 48

        seqNumber = int().from_bytes(data[4:8], byteorder='little')
        ackNumber = int().from_bytes(data[8:12], byteorder='little')

        length = int().from_bytes(data[12:16], byteorder='little')
        checksum = int().from_bytes(data[16:18], byteorder='little')

        payload = data[18:0]#.decode()  # bytes.decode(data[18:])
        # payload = ''
        return segment(sin=sin, fin=fin, ack=ack, rst=rst, seqNumber=seqNumber,
                       ackNumber=ackNumber, length=length, checkSum=checksum,
                       payload=payload)

    def __bytes__(self):
        return self.getSegment()


if __name__ == "__main__":
    print(segment(sin=1, ack=1).getSegment())
