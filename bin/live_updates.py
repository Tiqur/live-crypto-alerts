from unicorn_binance_websocket_api.unicorn_binance_websocket_api_manager import BinanceWebSocketApiManager

def live_updates(intervals, tokens, exchange):
    binance_websocket_api_manager = BinanceWebSocketApiManager(exchange=exchange)
    parsed_intervals = list(map(lambda i: f"kline_{i}", intervals))
    binance_websocket_api_manager.create_stream(parsed_intervals, tokens)

    # Actually get the live data
    while True:
        oldest_stream_data_from_stream_buffer = binance_websocket_api_manager.pop_stream_data_from_stream_buffer()
        if oldest_stream_data_from_stream_buffer:
            print(oldest_stream_data_from_stream_buffer)

