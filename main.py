from binance.client import Client
from dotenv import load_dotenv
from bin.TokenAnalysis import *
import os, time


# Load env variables
load_dotenv()
client = Client(os.getenv('API_KEY'), os.getenv('API_SECRET'))


# Coins to watch
watchlist = ['DOGEUSDT', 'BTCUSDT', 'ETHUSDT']
# trade, kline_1m, etc
intervals = ['kline_1m']


# Moving average intervals
ma_intervals = [9, 13, 21, 55]
# Amount of data relative to maximum interval to download. ( max_interval * precision )
# So if max_interval equals 55 and precision equals 2, then it would download 110 records for each interval
precision = 4
time_intervals = [Client.KLINE_INTERVAL_1MINUTE]




for token in watchlist:
    token_analysis = TokenAnalysis(client, token, time_intervals, ma_intervals, precision)
    token_analysis.download_history()
    token_analysis.calc_emas()



    


#from unicorn_binance_websocket_api.unicorn_binance_websocket_api_manager import BinanceWebSocketApiManager
#
#binance_websocket_api_manager = BinanceWebSocketApiManager(exchange="binance.com")
#binance_websocket_api_manager.create_stream(['kline_1m'], ['dogeusdt'])
#
#while True:
#    oldest_stream_data_from_stream_buffer = binance_websocket_api_manager.pop_stream_data_from_stream_buffer()
#    if oldest_stream_data_from_stream_buffer:
#        print(oldest_stream_data_from_stream_buffer)




