from utils.globals import testing, keyword_noti
from discord.ext import commands
from models.announcement import Announcement
from modules.message.announcement import announcement_create
import asyncio

def send_message(document: Announcement, bot: commands.Bot) -> None:
    for guild in bot.guilds:
        if testing and guild.id != 1399576991874809866:
            continue

        target_channel = None
        for channel in guild.text_channels:
            if any(keyword in channel.name.lower() for keyword in keyword_noti):
                target_channel = channel
                break

        if target_channel is None and len(guild.text_channels) > 0:
            target_channel = guild.text_channels[0]

        if target_channel is not None:
            coroutine = target_channel.send(announcement_create(document))
            asyncio.run_coroutine_threadsafe(coroutine, bot.loop)