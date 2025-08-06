import threading
from datetime import timezone, datetime, timedelta

import discord.errors
from dotenv import load_dotenv
import asyncio
from os import system
from modules.api_crawler import APICrawler
from services.announcement_service import AnnouncementService
from services.cookies_service import CookiesService
from services.member_service import MemberService
from services.request_service import RequestService
from services.student_service import StudentService
from services.study_history_service import StudyHistoryService
from utils.discordInit import create_bot
from modules.watch import watch_stream
from discord.ext import commands, tasks
from fastapi import FastAPI
import uvicorn
from utils.followup_send import FollowUpSend
import os
from modules.commands import Commands
from utils.globals import testing
from utils.http import HTTPHandler
import time
import logging

load_dotenv()
format_logging = '%(asctime)s: %(message)s'
logging.basicConfig(format=format_logging, level=logging.INFO, datefmt="%H:%M:%S")
app = FastAPI()
time_loop = None
time_sleep = None
discord_token = None
if testing:
    time_loop = 10
    time_sleep = 2
    discord_token = os.environ["DISCORD_TOKEN_SECONDARY"]
else:
    time_loop = 3 * 60
    time_sleep = 15
    discord_token = os.environ["DISCORD_TOKEN_PRIMARY"]
load_dotenv()
bot: commands.Bot = create_bot(prefix="/")
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


@app.head("/")
async def root():
    return {"status": "running"}
@app.get("/")
async def get_root():
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
    logging.info("crawler_loop: Starting")
    await announcement_service.compare_announcements()
    await api_crawler.student_loop()

async def check_run_time():
    now = datetime.now(timezone.utc) + timedelta(hours=7)  # giờ VN
    h = now.hour
    m = now.minute
    # Khung giờ chạy: 6:00-6:59, 12:00-12:59, 16:00-16:59
    if not ((h == 6) or (h == 12) or (h == 16)):
        logging.info(f"Outside run window: {h}:{m:02d}, sleeping 3 mins then exit")
        await asyncio.sleep(180)
    else:
        print(f"Within run window: {h}:{m:02d}, continue running")
        await asyncio.sleep(3600)
        logging.info('main: Exitting Application')
    logging.info("main: Exiting Application")
    os._exit(0)

def bg_thread_1():
    logging.info("Background thread watch_announcement_change: Starting")
    thread = threading.Thread(target=watch_stream.watch_announcement_change, args=(bot, announcement_service, ), daemon=True)
    thread.start()

def bg_thread_2():
    logging.info("Background thread watch_study_history_change: Starting")
    thread = threading.Thread(target=watch_stream.watch_study_history_change, args=(bot, study_history_service, member_service, ), daemon=True)
    thread.start()

async def start_discord():
    try:
        logging.info("start_discord: Starting")
        await bot.start(discord_token)
    except discord.errors.HTTPException:
        print("\n\n\nBLOCKED BY RATE LIMITS\nRESTARTING NOW\n\n\n")
        system('kill 1')


async def start_fastapi():
    logging.info("start_fastapi: Starting")
    config = uvicorn.Config(app, host="0.0.0.0", port=int(os.environ.get("PORT", 10000)), log_level="info", workers=1, loop="asyncio")
    server = uvicorn.Server(config)
    await server.serve()

async def main():
    logging.info('main: Starting')
    await asyncio.gather(
        start_fastapi(),
        start_discord()
    )

@bot.event
async def on_ready():
    if not getattr(bot, "synced", False):
        await bot.tree.sync()
        bot.synced = True
    logging.info(f'[BOT]: Ready at {bot.user}')
    bg_thread_1()
    bg_thread_2()
    await asyncio.sleep(time_sleep)
    crawler_loop.start()
    await check_run_time()

if __name__ == "__main__":
    asyncio.run(main())