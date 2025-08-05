from typing import Optional
from models.member import Member
from repositories.member_repo import MemberRepository
from utils.mongo import database_primary, database_secondary
from utils.globals import testing
class MemberService:
    def __init__(self):
        try:
            if not testing:
                self.repo = MemberRepository(database_primary)
            else:
                self.repo = MemberRepository(database_secondary)
        except Exception as e:
            import traceback
            print(repr(e))
            traceback.print_exc()

    def get_by_id(self, member_id: int) -> Optional[Member]:
        try:
            return Member.from_dict(self.repo.find_by_id(member_id))
        except Exception as e:
            import traceback
            print(repr(e))
            traceback.print_exc()

    def get_by_student_id(self, student_id: str) -> Optional[Member]:
        try:
            return Member.from_dict(self.repo.find_by_student_id(student_id))
        except Exception as e:
            import traceback
            print(repr(e))
            traceback.print_exc()

    def create(self, data: Member) -> Optional[str]:
        try:
            return str(self.repo.create(Member.to_dict(data)))
        except Exception as e:
            import traceback
            print(repr(e))
            traceback.print_exc()

    def update(self, member_id: int, member: Member) -> Optional[bool]:
        try:
            return self.repo.update(member_id, Member.to_dict(member))
        except Exception as e:
            import traceback
            print(repr(e))
            traceback.print_exc()