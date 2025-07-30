import asyncio
from discord.ext import commands
import discord
import os

class DiscordBot():
    def __init__(self):
        self.discord_token = os.getenv("DISCORD_TOKEN")
        self.intents = discord.Intents.default()
        self.bot = commands.Bot(command_prefix="/", intents=self.intents)
        
    async def start_up(self):
        await self.bot.start(self.discord_token)