from dataclasses import asdict
from datetime import datetime
from modules.crawler import announcement_crawler
from request_repo.announcement_repo import AnnouncementRepository
from models.announcement import Announcement, AnnouncementInput
from typing import List, Optional
from utils.mongo import database_primary, database_secondary
import traceback
from utils.globals import testing

class AnnouncementService:
    def __init__(self):
        if testing:
            self.repo = AnnouncementRepository(database_secondary)
        else:
            self.repo = AnnouncementRepository(database_primary)
    
    def get_all(self) -> List[Announcement]:
        return [Announcement.from_dict(ann_dict) for ann_dict in self.repo.find_all()]
    
    def exists(self, title: str, date_create: datetime) -> bool:
        return self.repo.exists(title, date_create)
        
    def get_by_id(self, _id: str) -> Optional[Announcement]:
        try:
            data = self.repo.find_by_id(_id)
            if not data:
                return None
            return Announcement.from_dict(data)
        except Exception as e:
            print("❌ Lỗi khi get_by_id:", e)
            traceback.print_exc()
            raise HTTPException(status_code=500, detail="Internal server error")
    
    def create(self, data: AnnouncementInput) -> str:
        return self.repo.create(asdict(data))
    
    def update (self, _id: str, data: Announcement) -> bool:
        return self.repo.update(_id, asdict(data))
    
    def delete(self, _id: str) -> bool:
        return self.repo.delete(_id)

    async def crawl_announcements(self) -> List[dict]:
        rs = []
        for ann_dict in [asdict(ann) for ann in announcement_crawler.crawl()]:
            if not self.exists(ann_dict.get("title"), ann_dict.get("date_create")):
                self.create(AnnouncementInput.from_dict(ann_dict))
                rs.append(ann_dict)
        return rs

    async def get_by_date_create_largest(self) -> Optional[Announcement]:
        return Announcement.from_dict(self.repo.find_by_date_create_largest())