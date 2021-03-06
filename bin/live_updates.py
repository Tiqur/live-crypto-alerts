from unicorn_binance_websocket_api.unicorn_binance_websocket_api_manager import BinanceWebSocketApiManager
from decimal import Decimal
from indicators.ema import *
from bin.ohlcv import *
import numpy as np
import datetime


def live_updates(intervals, ema_intervals, tokens, exchange, token_instances, alerts):
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

                # Price alerts
                alerts.append({"type": "price", "token": token, "price": str(ohlcv.close), "time": str(datetime.datetime.now(datetime.timezone.utc))})
                
                # For each token
                if token in token_instances:
                    token_instance = token_instances[token]
                    
                    # For each time_interval in token analysis instance history
                    for time_interval_instance in token_instance.time_interval_instances:
                        time_interval = time_interval_instance.candle_time_interval

                        for moving_average_instance in time_interval_instance.moving_average_instances:
                            ma_interval = moving_average_instance.ma_interval

                            # Calculate the time between the current time, and the previous candle's end time.
                            # This will show us if we should update the current candle's close_price, or create a new candle
                            time_between = ohlcv.start_time / 1000 - moving_average_instance.ohlcv[-1].end_time / 1000

                            # If on the same candle as last downloaded
                            if time_between < 0:
                                # Update price
                                moving_average_instance.ohlcv[-1].close = ohlcv.close
                            else:
                                # Previous ema
                                ema = np_ema(moving_average_instance.ohlcv[-1].close, moving_average_instance.emas[-1], moving_average_instance.ma_interval)

                                # Append previous ema
                                moving_average_instance.emas.append(ema)

                                # Append new candle 
                                moving_average_instance.ohlcv.append(ohlcv)

                                # Remove first element so that there is only ever ( ema_interval * percision ) amount of items in list
                                del moving_average_instance.ohlcv[0]
                                del moving_average_instance.emas[0]
                
                        
                        # Hold emas  
                        emas = {}

                        # For each ma interval
                        for moving_average_instance in time_interval_instance.moving_average_instances:
                            # Calculate live ema for each time interval
                            ema = np_ema(moving_average_instance.ohlcv[-1].close, moving_average_instance.emas[-1], moving_average_instance.ma_interval)
                            emas.update({moving_average_instance.ma_interval: ema})
                            #print(f"{moving_average_instance.ma_interval}: {round(ema, 5)}")

                        s = sorted(emas.items(), key=lambda x: x[1], reverse=True)
                        current4ma = list(map(lambda x: x[0], s))

                        # If 4ema changes, send alert
                        if time_interval_instance.last_4ma != current4ma:
                            time_interval_instance.last_4ma = current4ma

                            # Prevent false alert on startup
                            if time_interval_instance.first:
                                time_interval_instance.first = False
                            else:
                                alerts.append({"type": "alert", "token": token, "time": str(datetime.datetime.now(datetime.timezone.utc)), "interval": time_interval_instance.candle_time_interval, "4ma": current4ma})






