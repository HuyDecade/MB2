from pymongo import MongoClient
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

client = MongoClient(os.getenv('MONGO_URI'))
db = client['fraudDetectionDB']

# Transaction collection
transaction_collection = db['transactions']

def create_transaction(user_id, amount, location, timestamp):
    transaction = {
        'user_id': user_id,
        'amount': amount,
        'location': location,
        'timestamp': timestamp
    }
    transaction_collection.insert_one(transaction)

def get_transactions_by_user(user_id):
    return transaction_collection.find({'user_id': user_id})
