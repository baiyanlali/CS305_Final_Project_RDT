import RDTTimer


def time_out():
    print('test: ooh! time out!')


if __name__ == "__main__":
    timer = RDTTimer.RDTTimer(2, time_out)
    timer.start_to_count()
    print('test: can I go now ?')
