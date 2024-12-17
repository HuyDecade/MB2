from pymongo import MongoClient
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

client = MongoClient(os.getenv('MONGO_URI'))
db = client['fraudDetectionDB']

# User collection
user_collection = db['users']

def create_user(email, password):
    user = {
        'email': email,
        'password': password  # Mã hóa password trước khi lưu trong thực tế
    }
    user_collection.insert_one(user)

def find_user_by_email(email):
    return user_collection.find_one({'email': email})
