from binance.client import Client
from dotenv import load_dotenv
import os



# Load env variables
load_dotenv()
client = Client(os.getenv('API_KEY'), os.getenv('API_SECRET'))

