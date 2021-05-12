from binance.client import Client
from dotenv import load_dotenv
from bin.TokenAnalysis import *
from bin.live_updates import *
import threading
import os, time


# Load env variables
load_dotenv()
client = Client(os.getenv('API_KEY'), os.getenv('API_SECRET'))

# TODO: Create a config for this
# Coins to watch
watchlist = ['DOGEUSDT', 'BTCUSDT', 'ETHUSDT', 'BCHUSDT']

# Moving average intervals
ma_intervals = [9, 13, 21, 55]
# Amount of data relative to maximum interval to download. ( max_interval * precision )
# So if max_interval equals 55 and precision equals 2, then it would download 110 records for each interval
precision = 4
time_intervals = [Client.KLINE_INTERVAL_1MINUTE, Client.KLINE_INTERVAL_3MINUTE, Client.KLINE_INTERVAL_5MINUTE, Client.KLINE_INTERVAL_15MINUTE, Client.KLINE_INTERVAL_30MINUTE]


# Start websocket connections ( get live token data )
live_updates_thread = threading.Thread(target=live_updates, args=(time_intervals, watchlist, 'binance.com'))
live_updates_thread.start()


# Download historical token data
for token in watchlist:
    token_analysis = TokenAnalysis(client, token, time_intervals, ma_intervals, precision)
    token_analysis.download_history()
    token_analysis.calc_emas()




    





