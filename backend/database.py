from pymongo import MongoClient, errors
from dotenv import load_dotenv
import os
from dotenv import load_dotenv
from pymongo.errors import ConfigurationError, ServerSelectionTimeoutError

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")
print("MONGO_URI:", MONGO_URI)


try:
    # Connect to MongoDB with a timeout
    client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=5000)
    
    # Force connection on a request to confirm the server is reachable
    client.admin.command("ping")
    
    db = client["fortillm"]
    print("✅ Successfully connected to MongoDB")
    
except errors.ServerSelectionTimeoutError as e:
    print(f"❌ Could not connect to MongoDB: {e}")
    db = None  # Optional: set db to None or handle accordingly

except Exception as e:
    print(f"❌ Unexpected error during MongoDB connection: {e}")
    db = None
