from unicorn_binance_websocket_api.unicorn_binance_websocket_api_manager import BinanceWebSocketApiManager
from indicators.ema import *
from bin.ohlcv import *
import numpy as np


def live_updates(intervals, ema_intervals, tokens, exchange, token_instances):
    binance_websocket_api_manager = BinanceWebSocketApiManager(exchange=exchange)
    parsed_intervals = list(map(lambda i: f"kline_{i}", intervals))
    binance_websocket_api_manager.create_stream(parsed_intervals, tokens, output="UnicornFy")
    cache = {}

    # Actually get the live data
    while True:
        data = binance_websocket_api_manager.pop_stream_data_from_stream_buffer()
        
        # If data exists
        if data:
            
            # If data is valid token info
            if "kline" in data:
                k = data["kline"]
                ohlcv_data = [
                        k["kline_start_time"],
                        k["open_price"],
                        k["high_price"],
                        k["low_price"],
                        k["close_price"],
                        k["base_volume"],
                        k["kline_close_time"]
                    ]

                # Create ohlcv instance of data
                ohlcv = Ohlvc(ohlcv_data)
                token = data["symbol"]
                
                # For each token
                if token in token_instances:
                    token_instance = token_instances[token]
                    
                    # For each time_interval in token analysis instance history
                    for interval_history in token_instance.history:
                        time_between = ohlcv.start_time / 1000 - interval_history.ohlcv[-1].end_time / 1000
    
                        # If on the same candle as last downloaded
                        if time_between < 0:
                            # Update price
                            interval_history.ohlcv[-1].close = ohlcv.close
                        else:
                            # Append new candle 
                            interval_history.ohlcv.append(ohlcv)

                            # Remove first element so that there is only ever ( ema_interval * percision ) amount of items in list
                            del interval_history.ohlcv[0]
                

                        print(f"--------{token}--------")
                        # For each ma interval
                        for ma in ema_intervals:
                            # Calculate live ema for each time interval
                            ema = np_ema(interval_history.ohlcv[-1].close, interval_history.emas[-1], ma)
                            print(f"EMA {ma}: {ema}")

                    

                    




