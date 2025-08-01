import traceback

import discord

from models.member import Member
from models.student import Student
from modules.message.announcement import announcement_create
from services.announcement_service import AnnouncementService
from services.cookies_service import CookiesService
from services.member_service import MemberService
from services.request_service import RequestService
from services.student_service import StudentService
from utils.http import user_login
from utils.utils_function import UtilsFunction

class Commands:
    def __init__(self,
                 announcement_service: AnnouncementService,
                 student_service: StudentService,
                 member_service: MemberService,
                 request_service: RequestService,
                 cookie_service: CookiesService,
                 followup_messages
                 ):
        self.announcement_service = announcement_service
        self.student_service = student_service
        self.member_service = member_service
        self.followup_messages = followup_messages
        self.request_service = request_service
        self.cookie_service = cookie_service

    async def member_is_same(self, interaction, student_id: str) -> None:
        member = self.member_service.get_by_student_id(student_id)
        if member.member_id == interaction.user.id:
            await interaction.edit_original_response(content=self.followup_messages.success[1])
        else:
            old_member_id = member.member_id
            member.member_id = interaction.user.id
            member.student_id = student_id
            member.username = interaction.user.name
            self.member_service.update(old_member_id, member)
            await interaction.edit_original_response(content=self.followup_messages.success[1])

    async def error_handler(self, interaction: discord.Interaction, request_id, e, full_error):
        print("Lỗi khi xử lý lệnh")
        traceback.print_exc()
        await interaction.edit_original_response(content=self.followup_messages.failure[6])
        if request_id is not None:
            await self.request_service.update(_id=str(request_id), successful=False, e=str(e), full_error=full_error)
        else:
            await self.request_service.create(interaction, successful=False, e=str(e), full_error=full_error)


    async def new_noti(self, interaction):
        request_id = None
        try:
            await interaction.response.defer(ephemeral=False)
            request_id = await self.request_service.create(interaction)

            message = await announcement_create(await self.announcement_service.get_by_date_create_largest())
            if message is not None:
                await interaction.edit_original_response(content=message)
            else:
                await interaction.edit_original_response(content=self.followup_messages.failure[0])
        except Exception as e:
            full_error = traceback.format_exc()
            await self.error_handler(interaction, request_id, e, full_error)

    async def login(self, interaction, student_id: str, password: str):
        request_id = None
        try:
            await interaction.response.defer(ephemeral=True)
            request_id = await self.request_service.create(interaction)

            student_id = UtilsFunction.to_lower(student_id)
            cookies = await user_login(student_id, password)
            if cookies is not None:
                cookies_id = self.cookie_service.create(cookies)
                student = self.student_service.get_by_id(student_id)
                if student is not None:
                    if student.password == password:
                        if student.status:
                            await self.member_is_same(interaction, student_id)
                        else:
                            student.status = True
                            student.cookies_id = cookies_id
                            self.student_service.update(student_id, student)
                            await self.member_is_same(interaction, student_id)
                    else:
                        student.password = password
                        student.status = True
                        student.cookies_id = cookies_id
                        await self.member_is_same(interaction, student_id)
                else:
                    self.student_service.create(Student(student_id=student_id, password=password, status=True, cookies_id=cookies_id))
                    self.member_service.create(Member(member_id=interaction.user.id, student_id=student_id, username=interaction.user.name))
                    await interaction.edit_original_response(content=self.followup_messages.success[1])
            else:
                await interaction.edit_original_response(content=self.followup_messages.failure[2])
        except Exception as e:
            full_error = traceback.format_exc()
            await self.error_handler(interaction, request_id, e, full_error)


    async def logout(self, interaction):
        request_id = None
        try:
            await interaction.response.defer(ephemeral=True)
            request_id = await self.request_service.create(interaction)

            member = self.member_service.get_by_id(int(interaction.user.id))
            if member is not None:
                student_id = member.student_id
                student = self.student_service.get_by_id(student_id)
                status = student.status
                if status:
                    student.status = False
                    self.student_service.update(student_id, student)
                    await interaction.edit_original_response(content=self.followup_messages.success[2])
                else:
                    await interaction.edit_original_response(content=self.followup_messages.failure[5])
            else:
                await interaction.edit_original_response(content=self.followup_messages.failure[5])
        except Exception as e:
            full_error = traceback.format_exc()
            await self.error_handler(interaction, request_id, e, full_error)