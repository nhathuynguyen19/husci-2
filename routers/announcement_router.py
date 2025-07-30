
from fastapi import APIRouter, Query
from services.announcement_service import AnnouncementService
from typing import List
router = APIRouter()
service = AnnouncementService()

@router.get("/api/announcements")
def get_all() -> List[dict]:
    return [ann.to_dict() for ann in service.get_all()]

@router.get("/api/announcement")
def get_by_id(_id: str = Query(...)) -> dict:
    return service.get_by_id(_id).to_dict()

@router.get("/crawl/announcements")
async def crawl_announcements():
    return service.crawl_announcements()