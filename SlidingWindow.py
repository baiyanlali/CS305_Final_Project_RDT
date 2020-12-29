import Segment
import time
import threading


class SendingWindow:
    def __init__(self, window_size, datas, sender_time_out_method, window_base=0, time_out=1):
        self.datas = datas  # type: list # 发端全部data
        self.window_size = window_size  # 滑动窗口的大小
        self.window_base = window_base  # 滑动窗口的起始位置
        self.buffer = {}  # 滑动窗口内的所有值，用字典索引存储
        self.time = {}  # 设定进来每个包的初始时间
        self.time_out = time_out
        self.receive_last=False
        for i in range(window_base, min(window_base + window_size, len(datas))):
            try:
                self.buffer[i] = datas[i]
                self.time[i] = time.time()
            except IndexError:
                # print('SendingWindow: index is {} and len of datas is {}'.format(i,len(datas)))
                raise IndexError
        thread = threading.Thread(target=self.check_time_out, args=(time_out, sender_time_out_method))
        thread.start()

    def ack(self, ackNum):
        """
        当发端收到接收端的ack时，将窗口内对应块清空，然后检测滑动窗口起始点是否为空，若为空，则窗口起始点后移，直到起始点不为空
        若发送完毕，返回True
        若ack值不在滑动窗口内，则不做处理
        """

        win_begin = self.window_base
        win_end = self.window_base + self.window_size
        if ackNum not in range(win_begin, win_end):  # 判断ack是否在窗口内
            # print('sending_window: wrong ack num')
            return
        if ackNum == len(self.datas) - 1:  # 判断数据包是否传输完毕
            #TODO: May cause problems
            self.receive_last=True  #最后序号包已传入，若最后序号包不是最后传入包，则之后每次传入包做检测
            all_receive = True
            for seq, seg in self.buffer.items():
                if seg is None:
                    continue
                else:
                    all_receive=False
                    break
            if all_receive:
                print('sending_window: send over')
                del self.buffer[ackNum]
                del self.time[ackNum]
                return True

        self.buffer[ackNum] = None  # 将ack位置设为空
        if self.receive_last:#将每次传入的包做检测
            is_done=True
            for seq, seg in self.buffer.items():
                if seg is None:
                    pass
                else:
                    is_done=False
                    break
            if is_done:
                print('sending_window: send over')
                return True
        else:
            dataToSend = []
            while self.buffer[self.window_base] is None:  # 检测并调整窗口起始点
                del self.buffer[self.window_base]
                del self.time[self.window_base]
                self.window_base += 1

                if self.window_base + self.window_size <= len(self.datas):
                    self.buffer[self.window_base + self.window_size - 1] = \
                        self.datas[self.window_base + self.window_size - 1]
                    self.time[self.window_base + self.window_size - 1] = time.time()
                    dataToSend.append(self.datas[self.window_base + self.window_size - 1])
                else:
                    self.window_size -= 1  # 如果窗口已到达右边界，则使window_size-1以确保不越界
            return dataToSend

    def check_time_out(self, time_out, sender_time_out_method):

        while True:
            time_now = time.time()
            for i in range(self.window_base, min(self.window_base + self.window_size, len(self.datas))):
                if i in self.buffer.keys() and self.buffer[i] is not None:
                    off = time_now - self.time[i]
                    if off >= self.time_out:
                        sender_time_out_method(self.buffer[i],self)
                        self.time[i] = time_now
                        print('SlidingWindow_checkTimeOut: retransmit pkt{}'.format(i))
            time.sleep(0.2)
            # print('check_time_out:beep')


class ReceiveWindow:  # 收端所使用的sliding window
    def __init__(self, windowSize, windowBase=0):
        self.windowSize = windowSize
        self.windowBase = windowBase
        self.receiveBuffer = {}
        for i in range(0, self.windowSize):
            self.receiveBuffer[i] = None  # 字典buffer 用来储存已经收到的乱序数据包

    def addSegment(self, seqNum: int, segment) -> bool:  # 在buffer中添加收到的包,返回为真表示添加成功
        if seqNum >= self.windowBase and self.hasSegment(seqNum) is False:  # 在包的seqNum大于windowBase且没收到这个包的情况下，添加该包
            self.receiveBuffer[seqNum] = segment
            return True
        else:
            return False

    def checkBuffer(self) -> Segment.segment:  # 检查seqNum为windowBase的包是否已经收到，若是，则返回该包，同时在字典中删除该包
        if self.receiveBuffer[self.windowBase] is not None:
            segment = self.popSegment(self.windowBase)
            del self.receiveBuffer[self.windowBase]
            self.windowBase = self.windowBase + 1
            self.receiveBuffer[self.windowBase + self.windowSize - 1] = None
            return segment

    def popSegment(self, seqNum) -> Segment.segment:
        return self.receiveBuffer[seqNum]

    def needCheck(self) -> bool:
        if self.receiveBuffer[self.windowBase] is not None:
            return True
        else:
            return False

    def hasSegment(self, seqNum) -> bool:  # 检查缓存中是否已有这个包，若有，返回真，否则返回假
        if seqNum in self.receiveBuffer.keys():
            if self.receiveBuffer[seqNum] is not None:
                return True
            else:
                return False
        else:
            return False

    def checkFinish(self, seqNum) -> bool:  # 检查这个包以及之前所有的包是否已经收到
        if seqNum < self.windowBase:
            return True
        else:
            return False

    if __name__ == "__main__":
        sw = SendingWindow(3, [0, 1, 2, 3, 4, 5, 6, 7])
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
