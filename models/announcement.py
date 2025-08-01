from dataclasses import dataclass, asdict
from datetime import datetime
from typing import Optional

from bson import ObjectId

@dataclass
class AnnouncementInput:
    title: str
    content: str
    url: str
    date_create: datetime
    
    @classmethod
    def from_dict(cls, data: dict) -> Optional["AnnouncementInput"]:
        if data is None:
            return None
        return cls(
            title=data.get("title"),
            content=data.get("content"),
            url=data.get("url"),
            date_create=(
                data.get("date_create")
                if isinstance(data.get("date_create"), datetime)
                else datetime.fromisoformat(data.get("date_create"))
            ),
        )

@dataclass
class Announcement:
    title: str
    content: str
    url: str
    date_create: datetime
    _id: Optional[ObjectId] = None
    
    def to_dict(self) -> Optional[dict]:
        data = asdict(self)
        data["_id"] = str(self._id)
        return data
    
    @classmethod
    def from_dict(cls, data: dict) -> Optional["Announcement"]:
        if data is None:
            return None
        return cls(
            _id=ObjectId(data["_id"]) if "_id" in data and data["_id"] else None,
            title=data.get("title"),
            content=data.get("content"),
            url=data.get("url"),
            date_create=(
                data.get("date_create")
                if isinstance(data.get("date_create"), datetime)
                else datetime.fromisoformat(data.get("date_create"))
            ),
        )

