from binance.client import Client
from dotenv import load_dotenv
import os


# Load env variables
load_dotenv()
client = Client(os.getenv('API_KEY'), os.getenv('API_SECRET'))


# Coins to watch
watchlist = ['DOGEUSDT', 'BTCUSDT', 'ETHUSDT']
# trade, kline_1m, etc
intervals = ['kline_1m']
# Moving average intervals
ma_intervals = [9, 13, 21, 55]
time_interval = Client.KLINE_INTERVAL_1MINUTE

# Emas rely on previous emas.  Calculate extra for more percision
download_range = max(ma_intervals) * 2

# If 1 min, download last 100 min of data in 1 min intervals
# if 5 min, download last 500 min of data in 5 min intervals
# if 1 day, download last 100 days of data in 1 day intervals


# Download data
historical_data = client.get_historical_klines("DOGEUSDT", time_interval, "1 day ago UTC")
print(historical_data)

#from unicorn_binance_websocket_api.unicorn_binance_websocket_api_manager import BinanceWebSocketApiManager
#
#binance_websocket_api_manager = BinanceWebSocketApiManager(exchange="binance.com")
#binance_websocket_api_manager.create_stream(['kline_1m'], ['dogeusdt'])
#
#while True:
#    oldest_stream_data_from_stream_buffer = binance_websocket_api_manager.pop_stream_data_from_stream_buffer()
#    if oldest_stream_data_from_stream_buffer:
#        print(oldest_stream_data_from_stream_buffer)




