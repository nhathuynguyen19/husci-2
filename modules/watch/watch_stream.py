import asyncio

from modules.bot_send.bot_send import send_announcement_to_discord, send_study_history_to_discord
from services.announcement_service import AnnouncementService
from discord.ext import commands

from services.member_service import MemberService
from services.study_history_service import StudyHistoryService


def watch_announcement_change(bot: commands.Bot,
                              announcement_service: AnnouncementService
                              ) -> None:
    try:
        with announcement_service.repo.collection.watch() as stream:
            print("Listening for changes in 'announcements' collection...")
            for change in stream:
                document_id = str(change["documentKey"]["_id"])
                document = announcement_service.get_by_id(document_id)
                if document is not None:
                    send_announcement_to_discord(document, bot)

    except Exception as e:
        import traceback
        print(repr(e))
        traceback.print_exc()

def watch_study_history_change(bot: commands.Bot,
                               study_history_service: StudyHistoryService,
                               member_service: MemberService
                               ) -> None:
    try:
        with study_history_service.repo.collection.watch() as stream:
            print("Listening for changes in 'study_history' collection...")
            for change in stream:
                document_id = str(change["documentKey"]["_id"])
                document = study_history_service.get_by_object_id(document_id)
                if document is not None:
                    student_id = document.get("student_id")
                    member = member_service.get_by_student_id(student_id)
                    if member:
                        send_study_history_to_discord(document, bot=bot, user_id=member.member_id)

    except Exception as e:
        import traceback
        print(repr(e))
        traceback.print_exc()


