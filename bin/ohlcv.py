class Ohlvc():
    def __init__(self, data):
        self.start_time = data[0]
        self.open = float(data[1])
        self.high = float(data[2])
        self.low = float(data[3])
        self.close = float(data[4])
        self.volume = float(data[5])
        self.end_time = float(data[6])

