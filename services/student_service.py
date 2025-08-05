from typing import Optional, List

from models.student import Student
from repositories.student_repo import StudentRepository
from utils.mongo import database_primary, database_secondary
from utils.globals import testing
class StudentService:
    def __init__(self):
        try:
            if not testing:
                self.repo = StudentRepository(database_primary)
            else:
                self.repo = StudentRepository(database_secondary)
        except Exception as e:
            import traceback
            print(repr(e))
            traceback.print_exc()

    def get_by_id(self, student_id: str) -> Optional[Student]:
        try:
            return Student.from_dict(self.repo.find_by_id(student_id=student_id))
        except Exception as e:
            import traceback
            print(repr(e))
            traceback.print_exc()

    def get_by_status(self, status : bool = True) -> Optional[List[dict]]:
        try:
            return self.repo.find_by_status(status=status)
        except Exception as e:
            import traceback
            print(repr(e))
            traceback.print_exc()

    def create(self, data: Student) -> Optional[str]:
        try:
            return self.repo.create(Student.to_dict(data))
        except Exception as e:
            import traceback
            print(repr(e))
            traceback.print_exc()

    def update(self, student_id: str, student: Student) -> Optional[bool]:
        try:
            return self.repo.update(student_id, Student.to_dict(student))
        except Exception as e:
            import traceback
            print(repr(e))
            traceback.print_exc()
