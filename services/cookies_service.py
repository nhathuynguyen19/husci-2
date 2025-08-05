from typing import Optional

from bson import ObjectId

from repositories.cookies_repo import CookiesRepository
from utils.mongo import database_primary, database_secondary
from utils.globals import testing
class CookiesService:
    def __init__(self):
        try:
            if not testing:
                self.repo = CookiesRepository(database_primary)
            else:
                self.repo = CookiesRepository(database_secondary)
        except Exception as e:
            import traceback
            print(repr(e))
            traceback.print_exc()

    def create(self, data: dict) -> Optional[ObjectId]:
        try:
            return self.repo.create(data)
        except Exception as e:
            import traceback
            print(repr(e))
            traceback.print_exc()

    def get_by_id(self, _id: str) -> Optional[dict]:
        try:
            return self.repo.find_by_id(_id)
        except Exception as e:
            import traceback
            print(repr(e))
            traceback.print_exc()