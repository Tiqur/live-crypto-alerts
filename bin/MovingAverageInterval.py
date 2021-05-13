import numpy as np
from indicators.ema import *
from indicators.sma import *


class MovingAverageInterval():
    def __init__(self, ma_interval):
        self.ma_interval = ma_interval
        self.ohlcv = []
        self.emas = []


    def calc_emas(self):
            # Extract closing prices from specified interval
            get_closing_price = np.vectorize(lambda c: c.close)
            closing_prices = get_closing_price(self.ohlcv)
            
            # Calculate SMA for first range, then delete from list to avoid using data from the future
            data_range = closing_prices[:self.ma_interval]
            self.emas.append(np_sma(data_range))
            
            # List without the first (ma) elements
            new_data_range = closing_prices[self.ma_interval:]

            for i in range(len(new_data_range)):
                self.emas.append(np_ema(new_data_range[i], self.emas[-1], self.ma_interval))

