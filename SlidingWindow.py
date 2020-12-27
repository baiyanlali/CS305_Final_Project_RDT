import Segment


class sending_window:
    def __init__(self, window_size, window_base=0):
        self.window_size = window_size
        self.window_base = window_base
        self.buffer = dict.fromkeys(range(window_base
                                          , window_base + window_size), None)


class ReceiveWindow:
    def __init__(self, windowSize, windowBase=0):
        self.windowSize = windowSize
        self.windowBase = windowBase
        self.receiveBuffer = dict.fromkeys(range(windowBase, windowBase + windowSize), None)

    def addSegment(self, seqNum, segment):
        self.receiveBuffer[seqNum] = segment

    def checkBuffer(self) -> Segment.segment:
        if self.receiveBuffer[self.windowBase] is not None:
            segment = self.popSegment(self.windowBase)
            del self.receiveBuffer[self.windowBase]
            self.windowBase = self.windowBase + 1
            self.receiveBuffer[self.windowBase + self.windowSize] = None
            return segment

    def popSegment(self, seqNum) -> Segment.segment:
        return self.receiveBuffer[seqNum]
