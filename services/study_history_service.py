from typing import Optional, List
from repositories.study_history_repo import StudyHistoryRepository
from utils.globals import testing
from utils.mongo import database_primary, database_secondary


class StudyHistoryService:
    def __init__(self):
        try:
            if not testing:
                self.repo = StudyHistoryRepository(database_primary)
            else:
                self.repo = StudyHistoryRepository(database_secondary)
        except Exception as e:
            import traceback
            print(repr(e))
            traceback.print_exc()

    def get_by_id(self, course_id: str, student_id: str) -> Optional[dict]:
        try:
            return self.repo.find_by_id(course_id, student_id)
        except Exception as e:
            import traceback
            print(repr(e))
            traceback.print_exc()

    def get_by_object_id(self, _id: str) -> Optional[dict]:
        try:
            return self.repo.find_by_object_id(_id)
        except Exception as e:
            import traceback
            print(repr(e))
            traceback.print_exc()

    def get_by_student_id(self, student_id: str) -> Optional[List[dict]]:
        try:
            return self.repo.find_by_student_id(student_id)
        except Exception as e:
            import traceback
            print(repr(e))
            traceback.print_exc()

    def create(self, data: dict) -> Optional[dict]:
        try:
            return self.repo.create(data)
        except Exception as e:
            import traceback
            print(repr(e))
            traceback.print_exc()

    def update(self, course_id: str, student_id: str, data: dict) -> Optional[dict]:
        try:
            return self.repo.update(course_id, student_id, data)
        except Exception as e:
            import traceback
            print(repr(e))
            traceback.print_exc()