from pymongo import MongoClient
import asyncio

client = MongoClient('localhost', 27017)
db = client['chat_db']
