import threading
from dotenv import load_dotenv
import asyncio
from services.announcement_service import AnnouncementService
from services.cookies_service import CookiesService
from services.member_service import MemberService
from services.request_service import RequestService
from services.student_service import StudentService
from utils.discordInit import DiscordBot
from modules.watch import announcement_watch
from discord.ext import commands, tasks
from fastapi import FastAPI
import uvicorn
from utils.followup_send import FollowUpSend
import os
from modules.commands import Commands

app = FastAPI()
@app.get("/")
async def root():
    return {"status": "running"}

load_dotenv()
discord_bot = DiscordBot()
bot: commands.Bot = discord_bot.create_bot(prefix="/")
followup_messages = FollowUpSend()
announcement_service = AnnouncementService()
student_service = StudentService()
member_service = MemberService()
cookies_service = CookiesService()
request_service = RequestService()
commands_discord_bot = Commands(announcement_service,
                                student_service,
                                member_service,
                                request_service,
                                cookies_service,
                                followup_messages)

@bot.tree.command(name="new", description="Xem thông báo mới nhất")
async def new(ctx) -> None:
    await commands_discord_bot.new_noti(ctx)

@bot.tree.command(name="login", description="Đăng nhập")
async def login(ctx, student_id: str, password: str):
    await commands_discord_bot.login(ctx, student_id, password)

@bot.tree.command(name="logout", description="Đăng xuất")
async def logout(ctx):
    await commands_discord_bot.logout(ctx)

def start_background_thread():
    thread = threading.Thread(target=announcement_watch.watch_changes, args=(bot,), daemon=True)
    thread.start()

@tasks.loop(minutes=10)
async def ten_minutes():
    print("ten minutes started")
    await announcement_service.crawl_announcements()

async def start_discord():
    await bot.start(discord_bot.discord_token)

async def start_fastapi():
    config = uvicorn.Config(app, host="0.0.0.0", port=int(os.environ.get("PORT", 10000)), log_level="info")
    server = uvicorn.Server(config)
    await server.serve()

async def main():
    await asyncio.gather(
        start_discord(),
        start_fastapi()
    )

@bot.event
async def on_ready():
    print(f"[BOT] Ready as {bot.user}")
    if not getattr(bot, "synced", False):
        await bot.tree.sync()
        bot.synced = True
    ten_minutes.start()
    start_background_thread()

if __name__ == "__main__":
    asyncio.run(main())