from bin.IntervalEnum import *
import time


class TokenAnalysis():
    def __init__(self, client, token, time_intervals, ma_intervals):
        self.token = token
        self.client = client
        self.ma_intervals = ma_intervals
        self.time_intervals = time_intervals
        self.emas = []

    def download_history(self):
        # Emas rely on previous emas.  Calculate extra for more percision
        download_range = max(self.ma_intervals) * 2
        
        # Download data for each time_interval and moving average range
        for time_interval in self.time_intervals:

            # Convert binance kline to seconds
            interval_sec = interval_to_sec(time_interval) * download_range
            current_time = time.time()
            start_time = current_time - interval_sec
            historical_data = self.client.get_historical_klines(self.token, time_interval, str(start_time), str(current_time))
