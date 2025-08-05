from utils.globals import testing, keyword_noti
from discord.ext import commands
from models.announcement import Announcement
from modules.message.message import announcement_create
import asyncio
import re
import unicodedata


def convert_to_acronym(text):
    try:
        cleaned_text = re.sub(r"[^\w\s-]", "", text)
        words = cleaned_text.split()
        acronym = "".join(word[0].upper() for word in words)

        for i in range(len(acronym) - 1, 0, -1):
            if acronym[i] == "-":
                acronym = acronym[:i]

        return acronym
    except Exception as e:
        import traceback
        print(repr(e))
        traceback.print_exc()

def remove_accents(input_str):
    try:
        normalized_str = unicodedata.normalize('NFD', input_str)
        filtered_str = ''.join(c for c in normalized_str if unicodedata.category(c) != 'Mn')
        return filtered_str
    except Exception as e:
        import traceback
        print(repr(e))
        traceback.print_exc()

def send_announcement_to_discord(document: Announcement, bot: commands.Bot) -> None:
    try:
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
    except Exception as e:
        import traceback
        print(repr(e))
        traceback.print_exc()

def send_study_history_to_discord(document: dict,
                                        bot: commands.Bot,
                                        user_id: int) -> None:
    try:
        if testing and user_id != 767394443820662784:
            return
        user_coroutine = bot.fetch_user(user_id)
        future_user = asyncio.run_coroutine_threadsafe(user_coroutine, bot.loop)
        user = future_user.result(timeout=5)
        if user:
                course_name = convert_to_acronym(remove_accents(document.get("course_name")))
                qtht = document.get("qtht")
                course_attempt = int(document.get("course_attempt"))
                exam = None
                mark_sum = None
                if course_attempt <= 1:
                    exam = document.get("first_exam")
                    mark_sum = document.get("first_sum")
                else:
                    exam = document.get("second_exam")
                    mark_sum = document.get("second_sum")

                new_dict = {
                    "LopHP": course_name,
                    "QTHT": qtht,
                    "THI": exam,
                    "TONG": mark_sum
                }

                len_lhp = max(len(course_name), 5)
                len_qtht = max(len(qtht), 4)
                len_thi = max(len(exam), 3)
                len_tong = max(len(mark_sum), 4)

                markdown_table = f"```\n"
                markdown_table += f"|{'LopHP': <{len_lhp}}|{'QTHT': <{len_qtht}}|{'THI': <{len_thi}}|{'TONG': <{len_tong}}|\n"
                markdown_table += f"|{'-' * len_lhp}|{'-' * len_qtht}|{'-' * len_thi}|{'-' * len_tong}|\n"
                markdown_table += f"|{new_dict['LopHP']:<{len_lhp}}|{new_dict['QTHT']:<{len_qtht}}|{new_dict['THI']:<{len_thi}}|{new_dict['TONG']:<{len_tong}}|\n"
                markdown_table += f"```"

                coroutine = user.send(markdown_table)
                asyncio.run_coroutine_threadsafe(coroutine, bot.loop)
        else:
            return
    except Exception as e:
        import traceback
        print(repr(e))
        traceback.print_exc()
