
from pymongo.database import Database
from typing import Optional

class MemberRepository:
    def __init__(self, database: Database):
        self.collection = database["members"]

    def find_by_id(self, member_id: int) -> Optional[dict]:
        return self.collection.find_one({"member_id": member_id})

    def find_by_student_id(self, student_id: str) -> Optional[dict]:
        return self.collection.find_one({"student_id": student_id})

    def create(self, data: dict) -> str:
        data.pop("_id", None)
        result = self.collection.insert_one(data)
        return str(result.inserted_id)

    def update(self, member_id: int, data: dict) -> bool:
        data.pop("_id", None)
        result = self.collection.update_one({"member_id": member_id}, {"$set": data})
        return result.modified_count > 0