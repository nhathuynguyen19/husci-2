from dataclasses import dataclass, asdict, field
from datetime import datetime, timezone
from typing import Optional

from bson import ObjectId


@dataclass
class Request:
    server_id: Optional[int] = None
    channel_id: Optional[int] = None
    member_id: Optional[int] = None
    server_name: Optional[str] = None
    channel_name: Optional[str] = None
    member_name: Optional[str] = None
    date_created: Optional[datetime] = field(default_factory=lambda: datetime.now(timezone.utc))
    command: Optional[str] = None
    successful: bool = True
    error_message: Optional[str] = None
    full_error: Optional[str] = None
    _id: Optional[ObjectId] = None

    def to_dict(self) -> Optional[dict]:
        data = asdict(self)
        data["_id"] = str(self._id) if self._id else None
        return data

    @classmethod
    def from_dict(cls, data: dict) -> Optional["Request"]:
        if data is None:
            return None

        return cls (
            server_id=data.get("server_id"),
            channel_id=data.get("channel_id"),
            member_id=data.get("member_id"),
            server_name=data.get("server_name"),
            channel_name=data.get("channel_name"),
            member_name=data.get("member_name"),
            date_created=data.get("date_created"),
            command=data.get("command"),
            successful=data.get("successful"),
            error_message=data.get("error_message"),
            full_error=data.get("full_error"),
            _id=data.get("_id"),
        )
