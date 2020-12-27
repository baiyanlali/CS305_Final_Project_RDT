import threading


class RDTTimer:
    def __init__(self, end_time, time_out):
        self.end_time = end_time
        self.time_out = time_out
        self.t = threading.Timer(end_time,time_out)

    def start_to_count(self):
        self.t.start()
        print('RDTTimer: start to count')
