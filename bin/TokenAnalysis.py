from bin.IntervalEnum import *
from indicators.ema import *
import time

class TokenAnalysis():
    def __init__(self, client, token, time_intervals, ma_intervals, precision):
        self.token = token
        self.precision = precision
        self.client = client
        self.ma_intervals = ma_intervals
        self.time_intervals = time_intervals
        self.history = []
        self.emas = []

    def download_history(self):
        # Emas rely on previous emas.  Calculate extra for more precision
        download_range = max(self.ma_intervals) * self.precision
        
        # Download data for each time_interval and moving average range
        for time_interval in self.time_intervals:
            print(f"Downloading {time_interval} data for {self.token} {self.time_intervals.index(time_interval)+1}/{len(self.time_intervals)}")

            # Convert binance kline to seconds
            interval_sec = interval_to_sec(time_interval) * download_range
            current_time = time.time()
            start_time = current_time - interval_sec
            historical_data = self.client.get_historical_klines(self.token, time_interval, str(start_time), str(current_time))

            self.history += (time_interval, historical_data)

    def calc_emas(self):
        print(self.history)
        for i in range(len(self.history)):
            print(i)






