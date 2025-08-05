from dataclasses import asdict
from datetime import datetime
from modules.crawler import announcement_crawler
from repositories.announcement_repo import AnnouncementRepository
from models.announcement import Announcement, AnnouncementInput
from typing import List, Optional
from utils.mongo import database_primary, database_secondary
from utils.globals import testing

class AnnouncementService:
    def __init__(self):
        if testing:
            self.repo = AnnouncementRepository(database_secondary)
        else:
            self.repo = AnnouncementRepository(database_primary)
    
    def get_all(self) -> Optional[List[Announcement]]:
        try:
            return [Announcement.from_dict(ann_dict) for ann_dict in self.repo.find_all()]
        except Exception as e:
            import traceback
            print(repr(e))
            traceback.print_exc()
    
    def exists(self, title: str, date_create: datetime) -> Optional[bool]:
        try:
            return self.repo.exists(title, date_create)
        except Exception as e:
            import traceback
            print(repr(e))
            traceback.print_exc()
        
    def get_by_id(self, _id: str) -> Optional[Announcement]:
        try:
            data = self.repo.find_by_id(_id)
            if not data:
                return None
            return Announcement.from_dict(data)
        except Exception as e:
            import traceback
            print(repr(e))
            traceback.print_exc()
    
    def create(self, data: AnnouncementInput) -> Optional[str]:
        try:
            return self.repo.create(asdict(data))
        except Exception as e:
            import traceback
            print(repr(e))
            traceback.print_exc()
    
    def update (self, _id: str, data: Announcement) -> Optional[bool]:
        try:
            return self.repo.update(_id, asdict(data))
        except Exception as e:
            import traceback
            print(repr(e))
            traceback.print_exc()
    
    def delete(self, _id: str) -> Optional[bool]:
        try:
            return self.repo.delete(_id)
        except Exception as e:
            import traceback
            print(repr(e))
            traceback.print_exc()

    async def compare_announcements(self) -> Optional[List[dict]]:
        try:
            rs = []
            for ann_dict in [asdict(ann) for ann in announcement_crawler.crawl()]:
                if not self.exists(ann_dict.get("title"), ann_dict.get("date_create")):
                    self.create(AnnouncementInput.from_dict(ann_dict))
                    rs.append(ann_dict)
            return rs
        except Exception as e:
            import traceback
            print(repr(e))
            traceback.print_exc()

    async def get_by_date_create_largest(self) -> Optional[Announcement]:
        try:
            return Announcement.from_dict(self.repo.find_by_date_create_largest())
        except Exception as e:
            import traceback
            print(repr(e))
            traceback.print_exc()