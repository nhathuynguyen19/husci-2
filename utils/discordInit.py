from typing import Optional
from discord.ext import commands
import discord

def create_bot(prefix: str = "/") -> Optional[commands.Bot]:
    try:
        intents = discord.Intents.default()
        intents.members = True
        intents.message_content = True
        return commands.Bot(command_prefix=prefix, intents=intents)
    except Exception as e:
        import traceback
        print(repr(e))
        traceback.print_exc()