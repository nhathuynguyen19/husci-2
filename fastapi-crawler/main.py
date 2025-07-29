from fastapi import FastAPI, Query, HTTPException
from crawler import announcements
import threading
from dotenv import load_dotenv
from pymongo import MongoClient
import os
from bson import ObjectId
import discord
from discord.ext import commands
import asyncio
# uvicorn main:app --reload --port 10000

load_dotenv()

intents = discord.Intents.default()
bot = commands.Bot(command_prefix="/", intents=intents)
bot_ready = None
discord_loop = None

app = FastAPI()

testing = True

mongo_uri = os.getenv("MONGO_URI") 
discord_token = os.getenv("DISCORD_TOKEN")

database = MongoClient(mongo_uri)["husci"]
announcements_col = database["announcements"]

@app.get("/fetch/announcements")
async def crawl_announcements():
    await bot_ready
    try:
        return announcements.run(announcements_col)
    except Exception as e:
        print("Error: ", e)
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/announcement")
def select(id: str = Query(...)):
    return announcements_col.find_one({"_id": ObjectId(id)})

@bot.event
async def on_ready():
    global discord_loop, bot_ready
    discord_loop = asyncio.get_running_loop()
    bot_ready = asyncio.Event()
    bot_ready.set()
    print(f"[BOT] Ready as {bot.user}")

def start_background_thread():
    def runner():
        while bot_ready is None:
            pass
        asyncio.run_coroutine_threadsafe(bot_ready.wait(), discord_loop).result()
        announcements.watch_changes(announcements_col, bot, testing)
    threading.Thread(target=runner, daemon=True).start()

    
@app.on_event("startup")
async def on_startup():
    asyncio.create_task(bot.start(discord_token))
    start_background_thread()
    

