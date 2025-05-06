from pymongo import MongoClient
import os
from dotenv import load_dotenv
from pymongo.errors import ConfigurationError, ServerSelectionTimeoutError

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")
print("MONGO_URI:", MONGO_URI)

try:
    client = MongoClient(MONGO_URI)
    db = client["fortillm"]
    print("Connected to MongoDB successfully!")
except ConfigurationError as e:
    print(f"Configuration Error: {e}")
except ServerSelectionTimeoutError as e:
    print(f"Server Selection Timeout: {e}")
except Exception as e:
    print(f"Unexpected Error: {e}")