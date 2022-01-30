from dotenv import find_dotenv, load_dotenv
import os
from pymongo import MongoClient

load_dotenv(find_dotenv())

def connectDB():
    return MongoClient(os.getenv('MONGODB_CONNECTION_STRING'))