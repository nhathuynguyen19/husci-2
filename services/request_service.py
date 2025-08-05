from typing import Optional

import discord
from bson import ObjectId

from repositories.request_repo import RequestRepository
from utils.mongo import database_primary, database_secondary
from utils.globals import testing
from models.request import Request
class RequestService:
    def __init__(self):
        try:
            if not testing:
                self.repo = RequestRepository(database_primary)
            else:
                self.repo = RequestRepository(database_secondary)
        except Exception as e:
            import traceback
            print(repr(e))
            traceback.print_exc()

    async def create(self, interaction: discord.Interaction, successful : bool = True, e: Optional[str] = None, full_error : Optional[str] = None) -> Optional[ObjectId]:
        try:
            guild = interaction.guild
            channel = interaction.channel

            channel_name = channel.name if channel and hasattr(channel, "name") else "DM"
            server_name = guild.name if guild else "DM"

            data = Request(
                server_id=guild.id if guild else None,
                channel_id=channel.id if channel else None,
                member_id=interaction.user.id,
                server_name=server_name,
                channel_name=channel_name,
                member_name=interaction.user.name,
                successful=successful,
                command=str(interaction.command.name),
                error_message=str(e),
                full_error=full_error
            )
            return self.repo.create(Request.to_dict(data))

        except Exception as e:
            import traceback
            print(repr(e))
            traceback.print_exc()

    async def update(self, _id: str, successful: bool = False, e: Optional[str] = None, full_error : Optional[str] = None) -> Optional[bool]:
        try:
            return self.repo.update(_id, successful, e, full_error)
        except Exception as e:
            import traceback
            print(repr(e))
            traceback.print_exc()
