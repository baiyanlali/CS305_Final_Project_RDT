class segment:  # 定义传输报文的格式
    """
    [0] sin,fin,ack,rst 1bit,建立连接请求标志,1代表请求建立连接;1bit,结束连接请求标志，1代表请求结束连接;1bit,1表示收到请求，包括sin和fin;rst为1bit，表示请求重新建立连接
    [1:4] seqNumber 32bit,表示将要发出的包的序号
    [5:8] ackNumber  32bit，表示想要收到的包的序号
    [9:12] Length  32bit,表示payload的长度，单位byte，不包括报文头
    [13:14] checksum 16bit,校验和
    """

    def __init__(self,sin=0,fin=0,ack=0,rst=0,seqNumber=0,ackNumber=0,length=0,checkSum=0,payload=''):  # 初始化报文
        self.sin = sin
        self.fin = fin
        self.ack = ack
        self.rst = rst

        self.seqNumber = seqNumber
        self.ackNumber = ackNumber

        self.length = length
        self.checksum = checkSum

        self.payload = payload

    def getLength(self):  # 求payload的长度
        self.length = len(self.payload)

    def getFlag(self) -> bytes:  # 将sin，fin,ack,rst打包成一个byte
        s = str(self.sin) + str(self.fin) + str(self.ack) + str(self.rst) + "0000"
        return s.encode()

    @staticmethod
    def getFlag(sin=0,fin=0,ack=0,rst=0):
        s = str(sin) + str(fin) + str(ack) + str(rst) + "0000"
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
    @staticmethod
    def payloadToByte(payload) -> bytes:  # 将payload转换成bytes
        s = payload
        return s.encode()

    def getSegment(self) -> bytes:  # 将整个报文转换为bytes
        byte = self.getFlag() + self.seqNumber.to_bytes() + self.ackNumber.to_bytes() + self.length.to_bytes() + self.checksum.to_bytes() + self.payloadToByte()
    @staticmethod
    def getSegment(sin=0,fin=0,ack=0,rst=0,seqNumber=0,ackNumber=0,length=0,checksum=0,payload='') -> bytes:  # 将整个报文转换为bytes
        byte = segment.getFlag(sin,fin,ack,rst) + seqNumber.to_bytes() + ackNumber.to_bytes() + length.to_bytes() + checksum.to_bytes() + segment.payloadToByte()

    @staticmethod
    def parse(data:bytes) -> 'segment':
        sin = data[0].decode()
        fin = data[1].decode()
        ack = None
        rst = None

        seqNumber = None
        ackNumber = None

        length = None
        checksum = None

        payload = None


if __name__=="__main__":
    print(segment(ack=1).getSegment())