from binance.client import Client
from dotenv import load_dotenv
from bin.TokenAnalysis import *
from bin.live_updates import *
from progress.bar import Bar
import threading
import os, yaml
token_instances = {}


# Load env variables
load_dotenv()
client = Client(os.getenv('API_KEY'), os.getenv('API_SECRET'))

# Load yaml config
with open('config.yml', 'r') as ymlfile:
    try:
        config = yaml.safe_load(ymlfile)
    except yaml.YAMLError as err:
        print(err)
    
    # Start websocket connections ( get live token data )
    live_updates_thread = threading.Thread(target=live_updates, args=(config['time_intervals'], config['watchlist'], 'binance.com', token_instances))
    live_updates_thread.start()

    # Download historical token data
    for token in config['watchlist']:
        print(f"Downloading data for {token}...")

        progress_bar = Bar('', 
                max=(len(config['time_intervals']) * len(config['ema_intervals'])),
                fill='█',
                suffix='%(percent).1f%% - %(eta)ds')

        token_analysis = TokenAnalysis(client, token, config['time_intervals'], config['ema_intervals'], config['precision'], progress_bar)
        token_analysis.download_history()
        token_analysis.calc_emas()
        token_instances.update({token: token_analysis})
