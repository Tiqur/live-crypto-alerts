from bin.IntervalEnum import *
from bin.TimeInterval import *
from bin.MovingAverageInterval import *
from indicators.ema import *
from indicators.sma import *
from bin.ohlcv import *
import numpy as np
import time, sys

class Token():
    def __init__(self, client, token, time_ranges, ma_ranges, precision, progress_bar):
        self.token = token
        self.precision = precision
        self.client = client
        self.ma_ranges = ma_ranges
        self.time_ranges = time_ranges
        self.progress_bar = progress_bar
        self.history = []

    def __repr__(self):
        return(f"""

-------Token-------
Token: {self.token}
Precision: {self.precision}
Moving Average Intervals: {self.ma_ranges}
Time Intervals: {self.time_ranges}
History: {self.history}\n
""")

    def download_history(self):
        # Download data for each time_range and moving average range
        for time_range in self.time_ranges:

            # Initialize interval history
            ih = TimeInterval(time_range)

            # Optimize downloads by only downloaded the necessary data per token
            for ma_range in self.ma_ranges:

                # Fill progress bar
                self.progress_bar.next()

                # Emas rely on previous emas.  Calculate extra for more precision
                download_range = ma_range * self.precision

                # Convert binance kline to seconds
                interval_sec = interval_to_sec(time_range) * download_range
                historical_data = self.client.get_historical_klines(self.token, time_range, f'{interval_sec} seconds ago UTC')

                # Test if download is optimized
                #print(f"{len(historical_data)} / {ma_range}: {len(historical_data) / ma_range} == {self.precision}")
        

                # Organize data
                for data in historical_data:
                    ih.ohlcv.append(Ohlvc(data))
                
            self.history.append(ih)

        # End progress bar
        self.progress_bar.finish()
        # Delete progress bar
        sys.stdout.write("\033[F") #back to previous line 
        sys.stdout.write("\033[K") #clear line 



    def calc_emas(self):
        for time_interval in self.history:
            # Extract closing prices from specified interval
            get_closing_price = np.vectorize(lambda c: c.close)
            closing_prices = get_closing_price(time_interval.ohlcv)
            
            # For each ma interval
            for ma in self.ma_ranges:

                # Calculate SMA for first range, then delete from list to avoid using data from the future
                data_range = closing_prices[:ma]
                time_interval.emas.append(np_sma(data_range))
                
                # List without the first (ma) elements
                new_data_range = closing_prices[ma:]

                for i in range(len(new_data_range)):
                    time_interval.emas.append(np_ema(new_data_range[i], time_interval.emas[-1], ma))
                    
                    
