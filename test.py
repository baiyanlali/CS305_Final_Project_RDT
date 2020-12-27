import RDTTimer
import Segment


def time_out(*args):
    print('test: ooh! time out!')
    print('test:',args[0])


if __name__ == "__main__":
    timer = RDTTimer.RDTTimer(segment=Segment.segment(ack=1), end_time=2, time_out=time_out)
    timer.start_to_count()
    print('test: can I go now ?')
