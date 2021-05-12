from unicorn_binance_websocket_api.unicorn_binance_websocket_api_manager import BinanceWebSocketApiManager
from bin.ohlcv import *

def live_updates(intervals, tokens, exchange, token_instances):
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
                    
                    print(token_instance.history[-1].ohlcv[-1].close)

                    # For each time_interval in token analysis instance history
                    for time_interval in token_instance.history:
                        time_between = ohlcv.start_time / 1000 - time_interval.ohlcv[-1].end_time / 1000
    
                        # If on the same candle as last downloaded
                        if time_between < 0:
                            # Update price
                            time_interval.ohlcv[-1].close = ohlcv.close
                        else:
                            # Append new candle 
                            time_interval.ohlcv.append(ohlcv)


                    

                    




