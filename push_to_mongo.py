import json
from pymongo import MongoClient

# Drop your actual MongoDB connection string here
MONGO_URI = "mongodb+srv://dattaatreya999_db_user:dattaDB999@bhajans.wek6ojf.mongodb.net/ragacron_db"

# Connect to the cluster
client = MongoClient(MONGO_URI)

# This will automatically create the database and collection if they don't exist
db = client["ragacron_db"]
collection = db["daily_bhajans"]

# Load the perfect matches
with open('ready_for_mongo.json', 'r', encoding='utf-8') as f:
    valid_bhajans = json.load(f)

# Bulk insert them into the cloud
if valid_bhajans:
    collection.insert_many(valid_bhajans)
    print(f"Success. {len(valid_bhajans)} bhajans are now live in MongoDB.")
else:
    print("No data found to insert.")