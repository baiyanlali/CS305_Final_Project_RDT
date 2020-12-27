# import threading
# import Segment
#
#
# class RDTTimer:
#
#     def __init__(self, segment: Segment.segment, end_time, time_out):
#         self.seq = segment.seqNumber
#         self.end_time = end_time
#         self.time_out = time_out
#         self.segment = segment
#         #TODO: threading error
#         self.t = threading.Timer(self.end_time,self.time_out, [self.segment])
#
#     def reset(self,segment:Segment.segment,end_time):
#         self.seq = segment.seqNumber
#         self.end_time = end_time
#         self.segment = segment
#         del self.t
#         self.t = threading.Timer(self.end_time, self.time_out, [self.segment])
#
#     def start_to_count(self):
#         # pass
#         self.t.start()
#         # self.t.join()
#
#         # print('RDTTimer: start to count')
#
#     def cancel_count(self):
#         # pass
#         self.t.cancel()
#
#     def __str__(self):
#         return self.seq
