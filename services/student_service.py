from typing import Optional

from models.student import Student
from request_repo.student_repo import StudentRepository
from utils.mongo import database_primary, database_secondary
from utils.globals import testing
class StudentService:
    def __init__(self):
        if not testing:
            self.repo = StudentRepository(database_primary)
        else:
            self.repo = StudentRepository(database_secondary)

    def get_by_id(self, student_id: str) -> Optional[Student]:
        return Student.from_dict(self.repo.find_by_id(student_id))

    def create(self, data: Student) -> str:
        return self.repo.create(Student.to_dict(data))

    def update(self, student_id: str, student: Student) -> bool:
        return self.repo.update(student_id, Student.to_dict(student))
