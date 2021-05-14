from bin.IntervalEnum import *
from bin.TimeInterval import *
from bin.MovingAverageInterval import *
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
        self.time_interval_instances = []

    def __repr__(self):
        return(f"""

-------Token-------
Token: {self.token}
Precision: {self.precision}
Moving Average Intervals: {self.ma_ranges}
Time Intervals: {self.time_ranges}
History: {self.time_interval_instances}\n
""")

    def download_history(self):
        # Download data for each time_range and moving average range
        for time_range in self.time_ranges:

            # Fill progress bar
            self.progress_bar.next()

            # Initialize interval history
            ih = TimeInterval(time_range)

            # Emas rely on previous emas.  Calculate extra for more precision
            download_range = max(self.ma_ranges) + self.precision

            # Convert binance kline to seconds
            interval_sec = interval_to_sec(time_range) * download_range
            historical_data = self.client.get_historical_klines(self.token, time_range, f'{interval_sec} seconds ago UTC')
            #print(f"\nLen: {len(historical_data)} MaInterval: {ma_range} CandleInterval: {time_range}")

            # Optimize downloads by only downloaded the necessary data per token
            for ma_range in self.ma_ranges:

                # Initialize moving average interval instance
                mai = MovingAverageInterval(ma_range)

                # New data range
                new_range = historical_data[-(ma_range + self.precision):]

                # Organize data
                for data in new_range:
                    mai.ohlcv.append(Ohlvc(data))

                # Append moving average instance to TimeInterval
                ih.moving_average_instances.append(mai)

                # Fill progress bar
                self.progress_bar.next()

                # Test if download is optimized
                #print(f"{len(historical_data)} / {ma_range}: {len(historical_data) / ma_range} == {self.precision}")

            self.time_interval_instances.append(ih)

        # End progress bar
        self.progress_bar.finish()
        # Delete progress bar
        sys.stdout.write("\033[F") #back to previous line 
        sys.stdout.write("\033[K") #clear line 



    def calc_emas(self):
        for time_interval_instance in self.time_interval_instances:
            for ma_interval_instance in time_interval_instance.moving_average_instances:
                ma_interval_instance.calc_emas()


                    
                    
