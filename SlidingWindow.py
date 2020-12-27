import Segment

class sending_window:
    def __init__(self,window_size,window_base=0):
        self.window_size=window_size
        self.window_base=window_base
        self.buffer=dict.fromkeys(range(window_base
                                        ,window_base + window_size),None)



