from modules.bot_send.announcement import send_message
from services.announcement_service import AnnouncementService
from discord.ext import commands

service = AnnouncementService()

def watch_changes(bot: commands.Bot) -> None:
    with service.repo.collection.watch() as stream:
        print("Listening for changes in 'announcements' collection...")
        for change in stream:
            document_id = str(change["documentKey"]["_id"])
            document = service.get_by_id(document_id)
            if document is None:
                continue
            send_message(document, bot)