from pymongo import MongoClient
import os
from dotenv import load_dotenv

load_dotenv()

client = MongoClient(os.environ.get('URI_MONGODB'))

db = client['pishield_server']
