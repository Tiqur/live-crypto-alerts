class TimeInterval():
    def __init__(self, interval):
        self.candle_time_interval = interval
        self.moving_average_instances = []
        self.flag = 1

    def __repr__(self):
        return(f"""

-------IntervalHistory-------
Interval: {self.interval}
EMAs: {self.emas}
OHLVCs: {self.ohlcv}\n
""")
