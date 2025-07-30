from fastapi import FastAPI
import threading
from dotenv import load_dotenv
import asyncio
from routers import announcement_router
from utils.discordInit import DiscordBot
from modules.watch import announcement_watch

# uvicorn main:app --port 10000 --reload

load_dotenv()
app = FastAPI()
app.include_router(announcement_router.router)
discord_bot = DiscordBot()
bot = discord_bot.bot
app_ready = False
startup_event = None

@bot.event
async def on_ready():
    print(f"[BOT] Ready as {bot.user}")
    if startup_event:
        startup_event.set()

def start_background_thread():
    thread = threading.Thread(target=announcement_watch.watch_changes, args=(bot,), daemon=True)
    thread.start()
    
@app.on_event("startup")
async def on_startup():
    global startup_event, app_ready
    startup_event = asyncio.Event()
    asyncio.create_task(discord_bot.start_up())
    start_background_thread()
    await startup_event.wait()
    app_ready = True
    

