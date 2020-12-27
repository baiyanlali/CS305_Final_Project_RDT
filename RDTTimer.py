import threading
import Segment


class RDTTimer:
    def __init__(self, segment: Segment.segment, end_time, time_out):
        self.seq = segment.seqNumber
        self.end_time = end_time
        self.time_out = time_out
        self.segment = segment
        self.t = threading.Timer(self.end_time,self.time_out, [self.segment])

    def start_to_count(self):
        self.t.start()

        # print('RDTTimer: start to count')

    def cancel_count(self):
        self.t.cancel()

    def __str__(self):
        return self.seq
