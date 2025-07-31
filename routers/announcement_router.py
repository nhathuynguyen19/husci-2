
from fastapi import APIRouter, Query
from services.announcement_service import AnnouncementService
from typing import List
router = APIRouter()
service = AnnouncementService()

@router.get("/crawl/announcements")
async def crawl_announcements():
    return service.crawl_announcements()