import threading
import Segment

class RDTTimer:
    def __init__(self, segment:Segment.segment, end_time, time_out):
        self.end_time = end_time
        self.time_out = time_out
        self.segment=segment
        self.t = threading.Timer(end_time,time_out,[segment])

    def start_to_count(self):
        self.t.start()
        print('RDTTimer: start to count')
