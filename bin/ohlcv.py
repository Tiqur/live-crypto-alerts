class Ohlvc():
    def __init__(self, data):
        self.start_time = data[0]
        self.open = data[1]
        self.high = data[2]
        self.low = data[3]
        self.close = data[4]
        self.volume = data[5]
        self.end_time = data[6]

