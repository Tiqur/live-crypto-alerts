from unicorn_binance_websocket_api.unicorn_binance_websocket_api_manager import BinanceWebSocketApiManager

def live_updates():
    binance_websocket_api_manager = BinanceWebSocketApiManager(exchange="binance.com")
    binance_websocket_api_manager.create_stream(['kline_1m'], ['dogeusdt'])

    # Actually get the live data
    while True:
        oldest_stream_data_from_stream_buffer = binance_websocket_api_manager.pop_stream_data_from_stream_buffer()
        if oldest_stream_data_from_stream_buffer:
            print(oldest_stream_data_from_stream_buffer)

