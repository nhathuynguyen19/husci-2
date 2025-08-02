from dataclasses import dataclass, asdict
from datetime import datetime
from typing import Optional
from utils.utils_function import UtilsFunction
from bson import ObjectId


@dataclass
class Student:
    student_id: Optional[str] = None
    password: Optional[str] = None
    status: Optional[bool] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    gender: Optional[str] = None
    date_of_birth: Optional[datetime] = None
    place_of_birth: Optional[str] = None
    nationality: Optional[str] = None
    ethnicity: Optional[str] = None
    religion: Optional[str] = None
    citizen_id: Optional[str] = None
    id_card_issue_date: Optional[datetime] = None
    id_card_place_of_issue: Optional[str] = None
    phone_number: Optional[str] = None
    email: Optional[str] = None
    cookies_id: Optional[ObjectId] = None
    _id: Optional[ObjectId] = None

    def to_dict(self) -> Optional[dict]:
        data = asdict(self)
        data["_id"] = str(self._id) if self._id else None
        data["student_id"] = UtilsFunction.to_lower(data["student_id"])
        return data

    @classmethod
    def from_dict(cls, data: dict) -> Optional["Student"]:
        if data is None:
            return None

        return cls (
            student_id = UtilsFunction.to_lower(data.get("student_id")),
            password = data.get("password"),
            status = data.get("status"),
            first_name = data.get("first_name"),
            last_name = data.get("last_name"),
            gender = data.get("gender"),
            date_of_birth = data.get("date_of_birth"),
            place_of_birth = data.get("place_of_birth"),
            nationality = data.get("nationality"),
            ethnicity = data.get("ethnicity"),
            religion = data.get("religion"),
            citizen_id = data.get("citizen_id"),
            id_card_issue_date = data.get("id_card_issue_date"),
            id_card_place_of_issue = data.get("id_card_place_of_issue"),
            phone_number = data.get("phone_number"),
            email = data.get("email"),
            cookies_id = data.get("cookies_id"),
            _id = data.get("_id"),
        )
