import Segment


class sending_window:
    def __init__(self, window_size, window_base=0):
        self.window_size = window_size
        self.window_base = window_base
        self.buffer = dict.fromkeys(range(window_base
                                          , window_base + window_size), None)


class ReceiveWindow:  # 收端所使用的sliding window
    def __init__(self, windowSize, windowBase=0):
        self.windowSize = windowSize
        self.windowBase = windowBase
        self.receiveBuffer = dict.fromkeys(range(windowBase, windowBase + windowSize), None)  # 字典buffer 用来储存已经收到的乱序数据包

    def addSegment(self, seqNum, segment):  # 在buffer中添加收到的包
        if seqNum >= self.windowBase:
            self.receiveBuffer[seqNum] = segment

    def checkBuffer(self) -> Segment.segment:  # 检查seqNum为windowBase的包是否已经收到，若是，则返回该包，同时在字典中删除该包
        if self.receiveBuffer[self.windowBase] is not None:
            segment = self.popSegment(self.windowBase)
            del self.receiveBuffer[self.windowBase]
            self.windowBase = self.windowBase + 1
            self.receiveBuffer[self.windowBase + self.windowSize] = None
            return segment

    def popSegment(self, seqNum) -> Segment.segment:
        return self.receiveBuffer[seqNum]
