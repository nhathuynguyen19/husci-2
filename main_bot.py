import asyncio
import os
import threading
from os import system

import discord.errors
asyncio.set_event_loop_policy(asyncio.DefaultEventLoopPolicy())
import uvicorn
from discord.ext import commands, tasks
from dotenv import load_dotenv

from modules.api_crawler import APICrawler
from modules.commands import Commands
from modules.watch import watch_stream
from services.announcement_service import AnnouncementService
from services.cookies_service import CookiesService
from services.member_service import MemberService
from services.request_service import RequestService
from services.student_service import StudentService
from services.study_history_service import StudyHistoryService
from utils.discordInit import create_bot
from utils.followup_send import FollowUpSend
from utils.globals import testing
from utils.http import HTTPHandler

time_loop = None
time_sleep = None
discord_token = None
load_dotenv()
if testing:
    time_loop = 10
    time_sleep = 2
    discord_token = os.getenv("DISCORD_TOKEN_SECONDARY")
else:
    time_loop = 10 * 60
    time_sleep = 15
    discord_token = os.getenv("DISCORD_TOKEN_PRIMARY")
bot: commands.Bot = create_bot()
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
#
@bot.tree.command(name="new", description="Thông báo mới nhất")
async def new(ctx) -> None:
    await commands_discord_bot.new_noti(ctx)
#
@bot.tree.command(name="login", description="Đăng nhập")
async def login(ctx, student_id: str, password: str):
    await commands_discord_bot.login(ctx, student_id, password)
#
@bot.tree.command(name="logout", description="Đăng xuất")
async def logout(ctx):
    await commands_discord_bot.logout(ctx)
#
@bot.tree.command(name="scores", description="Lịch sử quá trình học tập")
async def scores(ctx):
    await commands_discord_bot.scores(ctx)
#
# @tasks.loop(seconds=time_loop)
# async def crawler_loop():
#     await announcement_service.compare_announcements()
#     await api_crawler.student_loop()
#
#
# def bg_thread_1():
#     thread = threading.Thread(target=watch_stream.watch_announcement_change, args=(bot, announcement_service, ), daemon=True)
#     thread.start()
#
# def bg_thread_2():
#     thread = threading.Thread(target=watch_stream.watch_study_history_change, args=(bot, study_history_service, member_service, ), daemon=True)
#     thread.start()
#
# async def start_discord():
#     try:
#         print("⏳ Starting Discord bot...")
#         await bot.start(discord_token)
#
#     except discord.errors.HTTPException as e:
#         print("🚫 HTTPException:", e)
#         if e.status == 429:  # Rate limit
#             print("🔁 BLOCKED BY RATE LIMITS — Restarting...")
#             await bot.close()  # Đóng bot để giải phóng resource
#             os.system('kill 1')  # Chỉ dùng nếu đang chạy trong Docker
#         else:
#             raise
#
#     except Exception as e:
#         print("🔥 Unhandled exception:", e)
#         await bot.close()
#         raise
# #
# async def main():
#     bot.run(discord_token)
#
@bot.event
async def on_ready():
    print(f"[BOT] Ready as {bot.user}")
    if not getattr(bot, "synced", False):
        await bot.tree.sync()
        bot.synced = True
    # bg_thread_1()
    # bg_thread_2()
    # await asyncio.sleep(time_sleep)
    # crawler_loop.start()
    # print("crawl loops started")
#
if __name__ == "__main__":
    bot.run(discord_token)