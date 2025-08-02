from typing import List, Optional
from bson import ObjectId
from datetime import datetime
from pymongo.database import Database

from models.announcement import Announcement


class AnnouncementRepository:
    def __init__(self, database: Database):
        self.collection = database["announcements"]

    def find_all(self) -> List[dict]:
        return list(self.collection.find())
    
    def exists(self, title: str, date_create: datetime) -> bool:
        return self.collection.find_one({
            "title": title,
            "date_create": date_create
        })

    def find_by_id(self, _id: str) -> Optional[dict]:
        return self.collection.find_one({"_id": ObjectId(_id)})

    def create(self, data: dict) -> str:
        result = self.collection.insert_one(data)
        return str(result.inserted_id)

    def update(self, _id: str, data: dict) -> bool:
        data.pop("_id", None)
        result = self.collection.update_one({"_id": ObjectId(_id)}, {"$set": data})
        return result.modified_count > 0

    def delete(self, _id: str) -> bool:
        result = self.collection.delete_one({"_id": ObjectId(_id)})
        return result.deleted_count > 0

    def find_by_date_create_largest(self) -> Optional[dict]:
        return self.collection.find_one(sort=[("date_create", -1)])