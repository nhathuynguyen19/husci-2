from dataclasses import dataclass, asdict
from typing import Optional

from bson import ObjectId

from utils.utils_function import UtilsFunction


@dataclass
class Member:
    member_id: Optional[int] = None
    username: Optional[str] = None
    student_id: Optional[str] = None
    _id: Optional[ObjectId] = None

    def to_dict(self) -> Optional[dict]:
        data = asdict(self)
        data["_id"] = str(self._id)
        data["student_id"] = UtilsFunction.to_lower(data["student_id"])
        data["member_id"] = UtilsFunction.to_lower(data["member_id"])
        return data

    @classmethod
    def from_dict(cls, data: dict) -> Optional["Member"]:
        if data is None:
            return None
        return cls (
            member_id = UtilsFunction.to_lower(data.get("member_id")),
            username = data.get("username"),
            student_id = UtilsFunction.to_lower(data.get("student_id")),
            _id = data.get("_id")
        )