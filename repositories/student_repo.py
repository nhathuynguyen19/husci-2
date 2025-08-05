from pymongo.database import Database
from typing import Optional, List


class StudentRepository:
    def __init__(self, database: Database):
        self.collection = database["students"]

    def find_by_id(self, student_id: str) -> Optional[dict]:
        return self.collection.find_one({"student_id": student_id})

    def find_by_status(self, status : bool = True) -> Optional[List[dict]]:
        return list(self.collection.find({"status": status}))

    def create(self, data: dict) -> str:
        data.pop("_id")
        result = self.collection.insert_one(data)
        return str(result.inserted_id)

    def update(self, student_id: str, data: dict) -> bool:
        data.pop("_id", None)
        result = self.collection.update_one({"student_id": student_id}, {"$set": data})
        return result.modified_count > 0