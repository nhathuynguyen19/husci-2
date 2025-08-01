from pymongo import MongoClient
from dotenv import load_dotenv
import os

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")
DATABASE_NAME_PRIMARY = os.getenv("DATABASE_NAME_PRIMARY")
DATABASE_NAME_SECONDARY = os.getenv("DATABASE_NAME_SECONDARY")

client = MongoClient(MONGO_URI)
database_primary = client[DATABASE_NAME_PRIMARY]
database_secondary = client[DATABASE_NAME_SECONDARY]
