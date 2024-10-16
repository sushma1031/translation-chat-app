from pymongo import MongoClient
import asyncio

async def connect():
  client = MongoClient('localhost', 27017)
  db = client.chat_db
  return db
