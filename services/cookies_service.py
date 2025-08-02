from typing import Optional

from bson import ObjectId

from models.student import Student
from request_repo.cookies_repo import CookiesRepository
from utils.mongo import database_primary, database_secondary
from utils.globals import testing
class CookiesService:
    def __init__(self):
        if not testing:
            self.repo = CookiesRepository(database_primary)
        else:
            self.repo = CookiesRepository(database_secondary)

    def create(self, data: dict) -> Optional[ObjectId]:
        return self.repo.create(data)
