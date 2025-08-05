import threading
from dotenv import load_dotenv
import asyncio

from modules.api_crawler import APICrawler
from services.announcement_service import AnnouncementService
from services.cookies_service import CookiesService
from services.member_service import MemberService
from services.request_service import RequestService
from services.student_service import StudentService
from services.study_history_service import StudyHistoryService
from utils.discordInit import DiscordBot
from modules.watch import watch_stream
from discord.ext import commands, tasks
from fastapi import FastAPI
import uvicorn
from utils.followup_send import FollowUpSend
import os
from modules.commands import Commands
from utils.globals import testing
from utils.http import HTTPHandler
import traceback

try:
    app = FastAPI()
    time_loop = None
    if testing:
        time_loop = 10
    else:
        time_loop = 10 * 60
    load_dotenv()
    discord_bot = DiscordBot()
    bot: commands.Bot = discord_bot.create_bot(prefix="/")
    followup_messages = FollowUpSend()
    announcement_service = AnnouncementService()
    student_service = StudentService()
    member_service = MemberService()
    cookies_service = CookiesService()
    request_service = RequestService()
    study_history_service = StudyHistoryService()
    http_handler = HTTPHandler(cookies_service=cookies_service,
                               student_service=student_service)
    api_crawler = APICrawler(http_handler=http_handler, study_history_service=study_history_service)
    commands_discord_bot = Commands(announcement_service=announcement_service,
                                    student_service=student_service,
                                    member_service=member_service,
                                    request_service=request_service,
                                    study_history_service=study_history_service,
                                    followup_messages=followup_messages,
                                    http_handler=http_handler,
                                    cookies_service=cookies_service)


    @app.get("/")
    async def root():
        return {"status": "running"}

    @bot.tree.command(name="new", description="Thông báo mới nhất")
    async def new(ctx) -> None:
        await commands_discord_bot.new_noti(ctx)

    @bot.tree.command(name="login", description="Đăng nhập")
    async def login(ctx, student_id: str, password: str):
        await commands_discord_bot.login(ctx, student_id, password)

    @bot.tree.command(name="logout", description="Đăng xuất")
    async def logout(ctx):
        await commands_discord_bot.logout(ctx)

    @bot.tree.command(name="scores", description="Lịch sử quá trình học tập")
    async def scores(ctx):
        await commands_discord_bot.scores(ctx)

    @tasks.loop(seconds=time_loop)
    async def crawler_loop():
        await announcement_service.compare_announcements()
        await api_crawler.student_loop()

    async def start_background_thread():
        thread1 = threading.Thread(target=watch_stream.watch_announcement_change, args=(bot, announcement_service, ), daemon=True)
        thread2 = threading.Thread(target=watch_stream.watch_study_history_change, args=(bot, study_history_service, member_service, ), daemon=True)
        thread1.start()
        thread2.start()

    async def start_discord():
        await bot.start(discord_bot.discord_token)

    async def start_fastapi():
        config = uvicorn.Config(app, host="0.0.0.0", port=int(os.environ.get("PORT", 10000)), log_level="info")
        server = uvicorn.Server(config)
        await server.serve()

    async def main():
        await asyncio.gather(
            start_discord(),
            start_fastapi(),
            start_background_thread()
        )

    @bot.event
    async def on_ready():
        print(f"[BOT] Ready as {bot.user}")
        if not getattr(bot, "synced", False):
            await bot.tree.sync()
            bot.synced = True
        crawler_loop.start()
        print("crawl loops started")

    if __name__ == "__main__":
        asyncio.run(main())
except Exception as e:
    print(repr(e))
    traceback.print_exc()