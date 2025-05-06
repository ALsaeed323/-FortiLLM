<<<<<<< HEAD
from pymongo import MongoClient
=======
from pymongo import MongoClient, errors
from dotenv import load_dotenv
>>>>>>> 18dbcd6e24e4f8734db6d598ca44252e53678b6a
import os
from dotenv import load_dotenv
from pymongo.errors import ConfigurationError, ServerSelectionTimeoutError

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")
print("MONGO_URI:", MONGO_URI)

<<<<<<< HEAD
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
=======

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


>>>>>>> 18dbcd6e24e4f8734db6d598ca44252e53678b6a
