from typing import Any, Coroutine

import aiohttp
from aiohttp import ClientSession
from bs4 import BeautifulSoup
from requests import Session

login_url = "https://student.husc.edu.vn/Account/Login"
message_url = "https://student.husc.edu.vn/Message/Inbox"
news_url = "https://student.husc.edu.vn/News"


async def fetch_soup(url: str, session: ClientSession) -> BeautifulSoup:
    async with session.get(url, timeout=30) as resp:
        return BeautifulSoup(await resp.text(), "html.parser")

async def user_login(student_id: str, password: str) -> bool:
    async with ClientSession() as session:
        soup = await fetch_soup(login_url, session)
        token = soup.find('input', {'name': '__RequestVerificationToken'})['value']
        login_data = {
            "loginID": student_id,
            "password": password,
            "__RequestVerificationToken": token
        }
        async with session.post(login_url, data=login_data, timeout=30) as login_resp:
            if "Account/Login" in str(login_resp.url):
                return False
            return login_resp.status == 200