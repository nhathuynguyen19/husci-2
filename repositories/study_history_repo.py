from bson import ObjectId
from pymongo.database import Database
from typing import Optional, List


class StudyHistoryRepository:
    def __init__(self, database: Database):
        self.collection = database["study_histories"]

    def find_by_id(self, course_id: str, student_id: str) -> Optional[dict]:
        return self.collection.find_one({"course_id": course_id, "student_id": student_id})

    def find_by_object_id(self, _id: str) -> Optional[dict]:
        return self.collection.find_one({"_id": ObjectId(_id)})

    def find_by_student_id(self, student_id: str) -> Optional[List[dict]]:
        return list(self.collection.find({"student_id": student_id}))

    def create(self, data: dict) -> Optional[dict]:
        result = self.collection.insert_one(data)
        return self.collection.find_one({"_id": result.inserted_id})
    def update(self, course_id: str, student_id: str, data: dict) -> Optional[dict]:
        self.collection.update_one({"course_id": course_id, "student_id": student_id}, {"$set": data})
        return self.find_by_id(course_id, student_id)