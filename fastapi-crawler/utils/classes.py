from dataclasses import dataclass, field
from datetime import datetime
from bson import ObjectId

@dataclass
class Announcement:
    title: str
    content: str
    url: str
    date_create: datetime