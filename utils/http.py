
from typing import Optional

from aiohttp import ClientSession
from bs4 import BeautifulSoup
from bson import ObjectId
from services.cookies_service import CookiesService
from services.student_service import StudentService
from models.student import Student

login_url = "https://student.husc.edu.vn/Account/Login"
message_url = "https://student.husc.edu.vn/Message/Inbox"
news_url = "https://student.husc.edu.vn/News"

async def fetch_soup_with_session(url: str, session: ClientSession) -> Optional[BeautifulSoup]:
    try:
        async with session.get(url, timeout=30) as resp:
            return BeautifulSoup(await resp.text(), "html.parser")
    except Exception as e:
        import traceback
        print(repr(e))
        traceback.print_exc()

class HTTPHandler:
    def __init__(self,
                 cookies_service: CookiesService,
                 student_service: StudentService,
                 ):
        self.cookies_service = cookies_service
        self.student_service = student_service

    async def user_login(self, student_id: str,
                         password: str
                         ) -> Optional[ObjectId]:
        try:
            async with ClientSession() as session:
                soup = await fetch_soup_with_session(url=login_url, session=session)
                token = soup.find('input', {'name': '__RequestVerificationToken'})['value']
                login_data = {
                    "loginID": student_id,
                    "password": password,
                    "__RequestVerificationToken": token
                }
                async with session.post(login_url, data=login_data, timeout=30) as login_resp:
                    if "Account/Login" in str(login_resp.url):
                        return None
                    cookies_base_str = session.cookie_jar.filter_cookies(login_resp.url)
                    cookies = {key: cookies_base_str[key].value for key in cookies_base_str}
                    cookies_id = self.cookies_service.create(cookies)
                    return cookies_id
        except Exception as e:
            import traceback
            print(repr(e))
            traceback.print_exc()

    async def fetch_soup_with_cookies(self,
                                      url: str,
                                      student: Student,
                                      cookies: dict
                                      ) -> Optional[BeautifulSoup]:
        try:
            async with ClientSession() as session:
                async with session.post(url, cookies=cookies) as resp:
                    if "Account/Login" in str(resp.url):
                        cookies_id = await self.user_login(student.student_id,
                                                      student.password)
                        student.cookies_id = cookies_id
                        self.student_service.update(student_id=student.student_id, student=student)
                        cookies = self.cookies_service.get_by_id(str(cookies_id))
                        return await self.fetch_soup_with_cookies(url, student, cookies)
                    else:
                        return BeautifulSoup(await resp.text(), "html.parser")
        except Exception as e:
            import traceback
            print(repr(e))
            traceback.print_exc()