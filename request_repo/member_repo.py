
from pymongo.database import Database
from typing import Optional

class MemberRepository:
    def __init__(self, database: Database):
        self.collection = database["members"]

    def find_by_id(self, member_id: int) -> Optional[dict]:
        return self.collection.find_one({"member_id": member_id})

    def create(self, data: dict) -> str:
        data.pop("_id", None)
        result = self.collection.insert_one(data)
        return str(result.inserted_id)