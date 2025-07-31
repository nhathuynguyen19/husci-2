import asyncio
from discord.ext import commands
import discord
import os
from utils.globals import testing

class DiscordBot:
    def __init__(self):
        if not testing:
            self.discord_token = os.getenv("DISCORD_TOKEN_PRIMARY")
        else:
            self.discord_token = os.getenv("DISCORD_TOKEN_SECONDARY")
        
    async def start_up(self, bot: commands.Bot):
        await bot.start(self.discord_token)

    def create_bot(self, prefix="/"):
        intents = discord.Intents.default()
        intents.members = True
        intents.message_content = True
        return commands.Bot(command_prefix=prefix, intents=intents)