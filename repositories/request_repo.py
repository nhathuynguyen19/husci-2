from typing import Optional

from bson import ObjectId
from pymongo.database import Database

class RequestRepository:
    def __init__(self, database: Database):
        self.collection = database["requests"]

    def create(self, data: dict) -> Optional[ObjectId]:
        data.pop("_id", None)
        result = self.collection.insert_one(data)
        return result.inserted_id

    def update(self, _id: str, successful: bool, error: Optional[str] = None, full_error : Optional[str] = None) -> bool:
        result = self.collection.update_one({"_id": ObjectId(_id)}, {"$set": {"successful": successful, "error": error, "full_error": full_error}})
        return result.modified_count > 0