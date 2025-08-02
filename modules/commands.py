import nextcord
import traceback
from models.member import Member
from models.student import Student
from modules.message.announcement import announcement_create
from services.announcement_service import AnnouncementService
from services.member_service import MemberService
from services.student_service import StudentService
from utils.http import user_login
from utils.utils_function import UtilsFunction

class Commands:
    def __init__(self,
                 announcement_service: AnnouncementService,
                 student_service: StudentService,
                 member_service: MemberService,
                 followup_messages
                 ):
        self.announcement_service = announcement_service
        self.student_service = student_service
        self.member_service = member_service
        self.followup_messages = followup_messages

    async def new_noti(self, ctx: nextcord.Interaction):
        try:
            try:
                if not ctx.response.is_done():
                    await ctx.response.defer(ephemeral=False, thinking=True)
            except Exception as e:
                print("Lỗi khi xử lý lệnh /new:")
                traceback.print_exc()
                await ctx.edit_original_response(content="❌ Lỗi hệ thống vui lòng thử lại sau!")
            message = await announcement_create(await self.announcement_service.get_by_date_create_largest())
            if message is not None:
                await ctx.edit_original_response(content=message)
            else:
                await ctx.edit_original_response(content=self.followup_messages.failure[0])
        except Exception as e:
            print("Lỗi khi xử lý lệnh /new:")
            traceback.print_exc()
            await ctx.edit_original_response(content="❌ Lỗi hệ thống vui lòng thử lại sau!")

    async def login(self, ctx: nextcord.Interaction, student_id: str, password: str):
        student_id = UtilsFunction.to_lower(student_id)
        try:
            try:
                if not ctx.response.is_done():
                    await ctx.response.defer(ephemeral=True, thinking=True)
            except Exception as e:
                print("Lỗi khi xử lý lệnh /login:")
                traceback.print_exc()
                await ctx.edit_original_response(content="❌ Lỗi hệ thống vui lòng thử lại sau!")
            student = await self.student_service.get_by_id(student_id)
            if student:
                if password == student.password:
                    student_condition = False
                    member_condition = False
                    if not student.status == True:
                        student.status = True
                        await self.student_service.update(str(student._id), student)
                    else:
                        student_condition = True

                    member = self.member_service.get_by_id(ctx.user.id)

                    if not member:
                        member = Member(member_id=ctx.user.id, username=ctx.user.name, student_id=student_id)
                        await self.member_service.create(member)
                    else:
                        member_condition = True

                    if student_condition and member_condition:
                        await ctx.edit_original_response(content=self.followup_messages.success[1])
                    else:
                        await ctx.edit_original_response(content=self.followup_messages.success[0])
                else:
                    await ctx.edit_original_response(content=self.followup_messages.failure[3])
            else:
                login_response = await user_login(student_id, password)
                if login_response:
                    student = Student(student_id=student_id, password=password, status=True)
                    member = Member(member_id=ctx.user.id, username=ctx.user.name, student_id=student_id)
                    await self.student_service.create(student)
                    await self.member_service.create(member)
                    await ctx.edit_original_response(content=self.followup_messages.success[0])
                else:
                    await ctx.followup.send(self.followup_messages.failure[2])
        except Exception as e:
            print("Lỗi khi xử lý lệnh /login:")
            traceback.print_exc()
            await ctx.edit_original_response(content="❌ Lỗi hệ thống vui lòng thử lại sau!")