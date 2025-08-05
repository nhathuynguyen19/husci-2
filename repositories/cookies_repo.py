from bson import ObjectId
from pymongo.database import Database
from typing import Optional


class CookiesRepository:
    def __init__(self, database: Database):
        self.collection = database["cookies"]

    def create(self, data: dict) -> Optional[ObjectId]:
        result = self.collection.insert_one(data)
        return result.inserted_id

    def find_by_id(self, _id: str) -> Optional[dict]:
        result = self.collection.find_one({"_id": ObjectId(_id)})
        result.pop("_id")
        return result