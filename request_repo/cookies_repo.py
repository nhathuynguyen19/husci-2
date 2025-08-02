from bson import ObjectId
from pymongo.database import Database
from typing import Optional


class CookiesRepository:
    def __init__(self, database: Database):
        self.collection = database["cookies"]

    def create(self, data: dict) -> Optional[ObjectId]:
        result = self.collection.insert_one(data)
        return result.inserted_id