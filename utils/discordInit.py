
from discord.ext import commands
import discord
import os
from utils.globals import testing

class DiscordBot:
    def __init__(self):
        try:
            if not testing:
                self.discord_token = os.getenv("DISCORD_TOKEN_PRIMARY")
            else:
                self.discord_token = os.getenv("DISCORD_TOKEN_SECONDARY")
        except Exception as e:
            import traceback
            print(repr(e))
            traceback.print_exc()

    @staticmethod
    def create_bot(prefix="/"):
        try:
            intents = discord.Intents.default()
            intents.members = True
            intents.message_content = True
            return commands.Bot(command_prefix=prefix, intents=intents)
        except Exception as e:
            import traceback
            print(repr(e))
            traceback.print_exc()