import Segment


class SendingWindow:
    def __init__(self, window_size, datas, window_base=0):
        self.datas = datas                          # type: list # 发端全部data
        self.window_size = window_size              #滑动窗口的大小
        self.window_base = window_base              #滑动窗口的起始位置
        self.buffer = {}                            #滑动窗口内的所有值，用字典索引存储
        for i in range(window_base, window_base + window_size):
            self.buffer[i] = datas[i]

    def ack(self, ackNum):
        """
        当发端收到接收端的ack时，将窗口内对应块清空，然后检测滑动窗口起始点是否为空，若为空，则窗口起始点后移，直到起始点不为空
        若发送完毕，返回True
        若ack值不在滑动窗口内，则不做处理
        """

        win_begin=self.window_base
        win_end=self.window_base+self.window_size
        if ackNum not in range(win_begin, win_end):     #判断ack是否在窗口内
            print('sending_window: wrong ack num')
            return
        if ackNum == len(self.datas)-1:                 #判断数据包是否传输完毕
            print('sending_window: send over')
            del self.buffer[ackNum]
            return True
        self.buffer[ackNum] = None                      #将ack位置设为空
        while self.buffer[self.window_base] is None:    #检测并调整窗口起始点
            del self.buffer[self.window_base]
            self.window_base += 1

            if self.window_base+self.window_size <= len(self.datas):
                self.buffer[self.window_base + self.window_size -1] = \
                    self.datas[self.window_base + self.window_size -1]
            else:
                self.window_size-=1                     #如果窗口已到达右边界，则使window_size-1以确保不越界


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



if __name__ == "__main__":
    sw = sending_window(3, [0,1, 2, 3, 4, 5, 6, 7])
    sw.ack(1)
    sw.ack(0)
    sw.ack(2)
    sw.ack(3)
    sw.ack(4)
    sw.ack(5)
    sw.ack(6)
    sw.ack(7)
    sw.ack(9)
    sw.ack(0)
