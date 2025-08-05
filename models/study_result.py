from datetime import datetime, timezone
from typing import Optional
from dataclasses import dataclass, field

from bson import ObjectId


@dataclass
class StudyHistory:
    course_id = Optional[str],
    course_url = Optional[str],
    course_name = Optional[str],
    course_url_me = Optional[str],
    credit_unit = Optional[int],
    course_attempt = Optional[int],
    qtht = Optional[float],
    first_exam = Optional[float],
    first_sum = Optional[float],
    second_exam = Optional[float],
    second_sum = Optional[float],
    student_id = Optional[str],
    date_created: Optional[datetime] = field(default_factory=lambda: datetime.now(timezone.utc))



