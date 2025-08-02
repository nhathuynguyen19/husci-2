import traceback

import discord

from models.member import Member
from models.student import Student
from modules.message.announcement import announcement_create
from services.announcement_service import AnnouncementService
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
                 followup_messages
                 ):
        self.announcement_service = announcement_service
        self.student_service = student_service
        self.member_service = member_service
        self.followup_messages = followup_messages
        self.request_service = request_service

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

            member = self.member_service.get_by_id(interaction.user.id)
            student_id = UtilsFunction.to_lower(student_id)
            student = self.student_service.get_by_id(member.student_id)
            student_condition = student.status
            if member is not None:
                if student_condition:
                    await interaction.edit_original_response(content=self.followup_messages.success[1])
                    return

            student = self.student_service.get_by_id(student_id)
            if student:
                member_condition = False
                if password == student.password:
                    if not student_condition == True:
                        student.status = True
                        await self.student_service.update(str(student.student_id), student)
                    else:
                        student_condition = True

                    member = self.member_service.get_by_id(interaction.user.id)

                    if not member:
                        member = Member(member_id=interaction.user.id, username=interaction.user.name, student_id=student_id)
                        await self.member_service.create(member)
                    else:
                        member_condition = True

                    if student_condition and member_condition:
                        await interaction.edit_original_response(content=self.followup_messages.success[1])
                    else:
                        await interaction.edit_original_response(content=self.followup_messages.success[0])
                else:
                    if not student_condition == True:
                        await interaction.edit_original_response(content=self.followup_messages.failure[3] )
                    else:
                        await interaction.edit_original_response(content=self.followup_messages.success[1])
            else:
                login_response = await user_login(student_id, password)
                if login_response:
                    student = Student(student_id=student_id, password=password, status=True)
                    member = Member(member_id=interaction.user.id, username=interaction.user.name, student_id=student_id)
                    await self.student_service.create(student)
                    await self.member_service.create(member)
                    await interaction.edit_original_response(content=self.followup_messages.success[0])
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
                    await self.student_service.update(student_id, student)
                    await interaction.edit_original_response(content=self.followup_messages.success[2])
                else:
                    await interaction.edit_original_response(content=self.followup_messages.failure[5])
            else:
                await interaction.edit_original_response(content=self.followup_messages.failure[5])
        except Exception as e:
            full_error = traceback.format_exc()
            await self.error_handler(interaction, request_id, e, full_error)