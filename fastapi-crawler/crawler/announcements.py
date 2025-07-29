import requests
from bs4 import BeautifulSoup
from dataclasses import asdict
from datetime import datetime
from utils.classes import Announcement
from utils.discord_message_create import announcement_create
from pymongo.collection import Collection
from discord.ext import commands
import asyncio

def run(collection):
    base_url = "https://ums.husc.edu.vn"
    response = requests.get(base_url)
    soup = BeautifulSoup(response.text, "html.parser")
    
    container_div = (
        soup.find('div', class_='panel-main-content')
            .find('div', class_='row')
            .find('div', class_='col-xs-12')
            .find('div', class_='container-fluid')
    )
    raw_announcements = container_div.find_all('div')
    
    result = []
    for raw_announcement in raw_announcements:
        a_tag = raw_announcement.select_one("p > a")
        small_tag = raw_announcement.select_one("p > small")
        
        title = a_tag.text.strip()
        content = raw_announcement.select("p")[1].text.strip()
        url = a_tag.get("href").strip()
        date_create = datetime.strptime(small_tag.text.strip("[]"), "%d/%m/%Y %H:%M")
        
        exists = collection.find_one({
            "title": title,
            "date_create": date_create
        })
        
        if not exists:
            announcement = Announcement(
                title=title,
                content=content,
                url=base_url + url,
                date_create=date_create
            )
            collection.insert_one(asdict(announcement))
            result.append(announcement)
    
    return result

def watch_changes(collection: Collection, bot: commands.Bot, testing: bool):
    
    with collection.watch() as stream:
        print("Listening for changes in 'announcements' collection...")
        for change in stream:
            document_id = change["documentKey"]["_id"]
            document = collection.find_one({"_id": document_id})
            if (document != None):
                announcement = Announcement(
                    title=document["title"],
                    content=document["content"],
                    url=document["url"],
                    date_create=document["date_create"]
                )
                
                keywords = [
                    "thông-báo", "thong-bao", "thông_báo", "thong_bao", "thongbao", "thôngbáo",
                    "announcement", "announcements", "notify", "notification", "noti", "news",
                    "updates", "update", "bulletin", "tin-tức", "tin_tức", "tin-tuc", "tin_tuc",
                    "notice", "thôngtin", "thongtin", "info", "informations", "inform"
                ]

                for guild in bot.guilds:
                    if testing and guild.id != 1399576991874809866:
                        continue

                    target_channel = None
                    for channel in guild.text_channels:
                        if any(keyword in channel.name.lower() for keyword in keywords):
                            target_channel = channel
                            break
                    
                    if target_channel is None and len(guild.text_channels) > 0:
                        target_channel = guild.text_channels[0]
                    
                    if target_channel is not None:
                        coroutine = target_channel.send(announcement_create(announcement))
                        asyncio.run_coroutine_threadsafe(coroutine, bot.loop)
                    