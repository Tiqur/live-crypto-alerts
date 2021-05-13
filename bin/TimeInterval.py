class TimeInterval():
    def __init__(self, interval):
        self.interval = interval
        self.emas = []
        self.ohlcv = []

    def __repr__(self):
        return(f"""

-------IntervalHistory-------
Interval: {self.interval}
EMAs: {self.emas}
OHLVCs: {self.ohlcv}\n
""")
