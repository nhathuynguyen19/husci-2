from typing import Optional
from models.member import Member
from models.student import Student
from request_repo.member_repo import MemberRepository
from utils.mongo import database_primary, database_secondary
from utils.globals import testing
class MemberService:
    def __init__(self):
        if not testing:
            self.repo = MemberRepository(database_primary)
        else:
            self.repo = MemberRepository(database_secondary)

    def get_by_id(self, member_id: int) -> Optional[Member]:
        return Member.from_dict(self.repo.find_by_id(member_id))

    def get_by_student_id(self, student_id: str) -> Optional[Member]:
        return Member.from_dict(self.repo.find_by_student_id(student_id))

    def create(self, data: Member) -> str:
        return str(self.repo.create(Member.to_dict(data)))

    def update(self, member_id: int, member: Member) -> bool:
        return self.repo.update(member_id, Member.to_dict(member))