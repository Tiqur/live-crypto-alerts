class TimeInterval():
    def __init__(self, interval):
        self.candle_time_interval = interval
        self.moving_average_instances = []
        self.last_4ma = []
        self.first = True

    def __repr__(self):
        return(f"""

-------IntervalHistory-------
Interval: {self.interval}
EMAs: {self.emas}
OHLVCs: {self.ohlcv}\n
""")
