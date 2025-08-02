from typing import Optional

import discord
from bson import ObjectId

from models.student import Student
from request_repo.request_repo import RequestRepository
from request_repo.student_repo import StudentRepository
from utils.mongo import database_primary, database_secondary
from utils.globals import testing
from models.request import Request
class RequestService:
    def __init__(self):
        if not testing:
            self.repo = RequestRepository(database_primary)
        else:
            self.repo = RequestRepository(database_secondary)

    async def create(self, interaction, successful : bool = True, e: Optional[str] = None, full_error : Optional[str] = None) -> Optional[ObjectId]:
        data = Request(server_id=interaction.guild.id,
                       channel_id=interaction.channel.id,
                       member_id=interaction.user.id,
                       server_name=interaction.guild.name,
                       channel_name=interaction.channel.name,
                       member_name=interaction.user.name,
                       successful=successful,
                       command=str(interaction.command.name),
                       error_message=e,
                       full_error=full_error
                       )
        return self.repo.create(Request.to_dict(data))

    async def update(self, _id: str, successful: bool = False, e: Optional[str] = None, full_error : Optional[str] = None) -> Optional[ObjectId]:
        return self.repo.update(_id, successful, e, full_error)
