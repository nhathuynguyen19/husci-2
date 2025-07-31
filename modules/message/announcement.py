from models.announcement import Announcement

async def announcement_create(announcement: Announcement):
    return "[" + announcement.title + "](" + announcement.url + ")\n`" + str(announcement.date_create.strftime("%d/%m/%Y %H:%M")) + "`\n" + announcement.content