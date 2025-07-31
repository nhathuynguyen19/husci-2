import traceback

import nextcord
import threading
from dotenv import load_dotenv
import asyncio
from services.announcement_service import AnnouncementService
from services.member_service import MemberService
from services.student_service import StudentService
from utils.discordInit import DiscordBot
from modules.watch import announcement_watch
from discord.ext import commands, tasks
import discord
from utils.http import user_login
from models.student import Student
from models.member import Member
from utils.globals import testing
from utils.mongo import database_primary, database_secondary
from modules.message.announcement import announcement_create
from utils.followup_send import FollowUpSend
from utils.utils_function import UtilsFunction
from nextcord import Interaction
import os

# uvicorn main:app --port 10000 --reload

load_dotenv()
discord_bot = DiscordBot()
bot: commands.Bot = discord_bot.create_bot(prefix="/")
followup_messages = FollowUpSend()

announcement_service = AnnouncementService()
student_service = StudentService()
member_service = MemberService()

@bot.tree.command(name="new", description="Xem thông báo mới nhất")
async def new(ctx: nextcord.Interaction) -> None:
    try:
        try:
            if not ctx.response.is_done():
                await ctx.response.defer(ephemeral=False, thinking=True)
        except Exception as e:
            traceback.print_exc()
        user_id = ctx.user.id
        message = await announcement_create(announcement_service.get_by_date_create_largest())
        if message is not None:
            await ctx.edit_original_response(content=message)
        else:
            await ctx.edit_original_response(content=followup_messages.failure[0])
    except Exception as e:
        traceback.print_exc()

@bot.tree.command(name="login", description="Đăng nhập")
async def login(ctx: nextcord.Interaction, student_id: str, password: str):
    student_id = UtilsFunction.to_lower(student_id)
    try:
        try:
            if not ctx.response.is_done():
                await ctx.response.defer(ephemeral=True, thinking=True)
        except Exception as e:
            traceback.print_exc()
        student = await student_service.get_by_id(student_id)
        if student:
            if password == student.password:
                student_condition = False
                member_condition = False
                if not student.status == True:
                    student.status = True
                    await student_service.update(str(student._id), student)
                else:
                    student_condition = True

                member = member_service.get_by_id(ctx.user.id)

                if not member:
                    member = Member(member_id=ctx.user.id, username=ctx.user.name, student_id=student_id)
                    await member_service.create(member)
                else:
                    member_condition = True

                if student_condition and member_condition:
                    await ctx.edit_original_response(content=followup_messages.success[1])
                else:
                    await ctx.edit_original_response(content=followup_messages.success[0])
            else:
                await ctx.edit_original_response(content=followup_messages.failure[3])
        else:
            login_response = await user_login(student_id, password)
            if login_response:
                student = Student(student_id=student_id, password=password, status=True)
                member = Member(member_id=ctx.user.id, username=ctx.user.name, student_id=student_id)
                await student_service.create(student)
                await member_service.create(member)
                await ctx.edit_original_response(content=followup_messages.success[0])
            else:
                await ctx.followup.send(followup_messages.failure[2])
    except Exception as e:
        traceback.print_exc()

def start_background_thread():
    thread = threading.Thread(target=announcement_watch.watch_changes, args=(bot,), daemon=True)
    thread.start()

@tasks.loop(minutes=10)
async def ten_minutes():
    await announcement_service.crawl_announcements()

@bot.event
async def on_ready():
    print(f"[BOT] Ready as {bot.user}")
    if not getattr(bot, "synced", False):
        await bot.tree.sync()
        bot.synced = True
    ten_minutes.start()

discord_bot.start_discord_bot(bot)