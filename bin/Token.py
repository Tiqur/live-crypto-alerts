from bin.IntervalEnum import *
from bin.ohlcv import *
from bin.IntervalHistory import *
from indicators.ema import *
from indicators.sma import *
import numpy as np
import time, sys

class Token():
    def __init__(self, client, token, time_intervals, ma_intervals, precision, progress_bar):
        self.token = token
        self.precision = precision
        self.client = client
        self.ma_intervals = ma_intervals
        self.time_intervals = time_intervals
        self.progress_bar = progress_bar
        self.history = []

    def __repr__(self):
        return(f"""

-------Token-------
Token: {self.token}
Precision: {self.precision}
Moving Average Intervals: {self.ma_intervals}
Time Intervals: {self.time_intervals}
History: {self.history}\n
""")

    def download_history(self):
        # Download data for each time_interval and moving average range
        for time_interval in self.time_intervals:

            # Optimize downloads by only downloaded the necessary data per token
            for ma_interval in self.ma_intervals:

                # Fill progress bar
                self.progress_bar.next()

                # Emas rely on previous emas.  Calculate extra for more precision
                download_range = ma_interval * self.precision

                # Convert binance kline to seconds
                interval_sec = interval_to_sec(time_interval) * download_range
                historical_data = self.client.get_historical_klines(self.token, time_interval, f'{interval_sec} seconds ago UTC')

                # Test if download is optimized
                #print(f"{len(historical_data)} / {ma_interval}: {len(historical_data) / ma_interval} == {self.precision}")
        
                # Initialize interval history
                ih = IntervalHistory(time_interval)

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
            for ma in self.ma_intervals:

                # Calculate SMA for first range, then delete from list to avoid using data from the future
                data_range = closing_prices[:ma]
                time_interval.emas.append(np_sma(data_range))
                
                # List without the first (ma) elements
                new_data_range = closing_prices[ma:]

                for i in range(len(new_data_range)):
                    time_interval.emas.append(np_ema(new_data_range[i], time_interval.emas[-1], ma))
                    
                    
