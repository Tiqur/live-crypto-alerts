from binance.client import Client
from dotenv import load_dotenv
from bin.Token import *
from bin.live_updates import *
from progress.bar import Bar
import threading
import os, yaml
import asyncio
import websockets
token_instances = {}
alerts = []


# Load env variables
load_dotenv()
client = Client(os.getenv('API_KEY'), os.getenv('API_SECRET'))

# Initialize server
async def server(websocket, path):
    while True:
        if alerts:
            await websocket.send(str(alerts.pop()))

# Start websocket server
def start_server():
    asyncio.set_event_loop(asyncio.new_event_loop())
    start_server = websockets.serve(server, "localhost", 5000)
    asyncio.get_event_loop().run_until_complete(start_server)
    asyncio.get_event_loop().run_forever()


# Load yaml config
with open('config.yml', 'r') as ymlfile:
    try:
        config = yaml.safe_load(ymlfile)
    except yaml.YAMLError as err:
        print(err)


    # Start local websocket server
    websocket_server = threading.Thread(target=start_server)
    websocket_server.start()

    # Start websocket connections ( get live token data )
    live_updates_thread = threading.Thread(target=live_updates, args=(config['time_intervals'], config['ema_intervals'], config['watchlist'], 'binance.com', token_instances, alerts))
    live_updates_thread.start()

    # Download historical token data
    for token in config['watchlist']:
        print(f"Downloading data for {token}...")

        progress_bar = Bar('', 
                max=(len(config['time_intervals']) * len(config['ema_intervals'])),
                fill='█',
                suffix='%(percent).1f%% - %(eta)ds')

        token_analysis = Token(client, token, config['time_intervals'], config['ema_intervals'], config['precision'], progress_bar)
        token_analysis.download_history()
        token_analysis.calc_emas()
        token_instances.update({token: token_analysis})
