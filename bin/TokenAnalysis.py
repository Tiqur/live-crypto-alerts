from bin.IntervalEnum import *
from bin.ohlcv import *
from bin.IntervalHistory import *
from indicators.ema import *
from indicators.sma import *
import numpy as np
import time

class TokenAnalysis():
    def __init__(self, client, token, time_intervals, ma_intervals, precision):
        self.token = token
        self.precision = precision
        self.client = client
        self.ma_intervals = ma_intervals
        self.time_intervals = time_intervals
        self.history = []

    def download_history(self):
        
        # Download data for each time_interval and moving average range
        for time_interval in self.time_intervals:
            print(f"Downloading {time_interval} data for {self.token} {self.time_intervals.index(time_interval)+1}/{len(self.time_intervals)}")

            # Optimize downloads by only downloaded the necessary data per token
            for ma_interval in self.ma_intervals:

                # Emas rely on previous emas.  Calculate extra for more precision
                download_range = ma_interval * self.precision

                # Convert binance kline to seconds
                interval_sec = interval_to_sec(time_interval) * download_range
                current_time = time.time()
                start_time = current_time - interval_sec
                historical_data = self.client.get_historical_klines(self.token, time_interval, str(start_time), str(current_time))
        
                # Initialize interval history
                ih = IntervalHistory(time_interval)

                # Organize data
                for data in historical_data:
                    ih.ohlcv.append(Ohlvc(data))
                
                self.history.append(ih)

    def calc_emas(self):
        for time_interval in self.history:
            # Extract closing prices from specified interval
            get_closing_price = np.vectorize(lambda c: c.close)
            closing_prices = get_closing_price(time_interval.ohlcv)
            
            # For each ma interval
            for ma in self.ma_intervals:
                for i in range(len(closing_prices)):
                    if i + ma <= len(closing_prices):
                        data_range = np.array(closing_prices[i:i+ma])
                        if i == 0:
                            time_interval.emas.append(np_sma(data_range))
                        else:
                            time_interval.emas.append(np_ema(closing_prices[i], time_interval.emas[i-1], ma))






