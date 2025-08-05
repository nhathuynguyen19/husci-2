import asyncio

from models.student import Student
from typing import List, Optional

from services.study_history_service import StudyHistoryService
from utils.http import HTTPHandler


class APICrawler:
    def __init__(self, http_handler: HTTPHandler, study_history_service: StudyHistoryService):
        self.http_handler = http_handler
        self.cookies_service = http_handler.cookies_service
        self.student_service = http_handler.student_service
        self.study_history_service = study_history_service
        self.url_inbox = "https://student.husc.edu.vn/Message/Inbox"
        self.url_history_study = "https://student.husc.edu.vn/Statistics/HistoryOfStudying"

    async def crawl_study_history_from_web(self, student: Student, cookies: dict) -> Optional[List[dict]]:
        try:
            soup = await self.http_handler.fetch_soup_with_cookies(self.url_history_study,
                                                             student=student,
                                                             cookies=cookies)
            if soup is None:
                return []
            data = []
            table = soup.find("table")
            tbody = table.find("tbody")
            rows = [tr for tr in tbody.find_all("tr") if len(tr.find_all("td")) > 2]
            for row in rows:
                tds = row.find_all("td")

                course_id = tds[1].get_text().strip()
                course_url = "https://student.husc.edu.vn" + tds[1].select_one("a")['href'].strip()
                course_name = tds[2].get_text().strip()
                course_url_me = "https://student.husc.edu.vn" + tds[2].select_one("a")['href'].strip()
                credit_unit = tds[3].get_text().strip()
                course_attempt = tds[4].get_text().strip()
                qtht = tds[5].get_text().strip()
                first_exam = tds[6].get_text().strip()
                first_sum = tds[7].get_text().strip()
                second_exam = tds[8].get_text().strip()
                second_sum = tds[9].get_text().strip()

                item = {
                    "course_id": course_id,
                    "course_url": course_url,
                    "course_name": course_name,
                    "course_url_me": course_url_me,
                    "credit_unit": credit_unit,
                    "course_attempt": course_attempt,
                    "qtht": qtht,
                    "first_exam": first_exam,
                    "first_sum": first_sum,
                    "second_exam": second_exam,
                    "second_sum": second_sum,
                    "student_id": student.student_id
                }
                data.append(item)
            return data
        except Exception as e:
            import traceback
            print(repr(e))
            traceback.print_exc()

    async def compare_study_history(self, student: Student, cookies: dict) -> Optional[List[dict]]:
        try:
            rs = []
            list_history = await self.crawl_study_history_from_web(student, cookies)
            for sr_dict in [sr_dict for sr_dict in list_history]:
                data = self.study_history_service.get_by_id(course_id=sr_dict.get("course_id"),
                                                            student_id=sr_dict.get("student_id")
                                                            )
                if data is None:
                    item = self.study_history_service.create(sr_dict)
                    rs.append(item)
                else:
                    data.pop("_id", None)
                    if sr_dict != data:
                        item = self.study_history_service.update(course_id=sr_dict.get("course_id"),
                                                          student_id=sr_dict.get("student_id"),
                                                          data=sr_dict
                                                          )
                        rs.append(item)
            return rs
        except Exception as e:
            import traceback
            print(repr(e))
            traceback.print_exc()

    async def student_loop(self):
        try:
            tasks = []
            for student in self.student_service.get_by_status():
                cookies = self.cookies_service.get_by_id(str(student.get("cookies_id")))
                tasks.append(self.compare_study_history(student=Student.from_dict(student), cookies=cookies))
            await asyncio.gather(*tasks)
        except Exception as e:
            import traceback
            print(repr(e))
            traceback.print_exc()