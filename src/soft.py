import asyncio
import logging

from telethon import TelegramClient
from telethon.errors import FloodWaitError
from telethon.tl.functions.channels import JoinChannelRequest

from src.asynctk import AsyncTkUtils
from src.client import Client


class Soft(AsyncTkUtils):
    def __init__(self, **kwargs):
        super().__init__()
        self.config = kwargs

        self.group_name = self.config.get("group_name", "")
        self.session_path = self.config.get("session_path", "")
        self.api_id = self.config.get("api_id", "")
        self.api_hash = self.config.get("api_hash", "")
        self.proxy = self.config.get("proxy", "")
        self.logger = self.config.get("logger", None)

        self.client = Client(self.session_path, self.api_id, self.api_hash, self.proxy)


    async def get_users_telegram(self):
        if not await self.client.is_valid():
            logging.error("Not valid session")
            self.message_box("Telegram Error", "Not valid session", type="error")
            return

        async with self.client as client:
            try:
                channel = await client.get_entity(self.group_name)
                await client(JoinChannelRequest(channel))
            except FloodWaitError as e:
                await asyncio.sleep(e.seconds + 5)
            except Exception as e:
                self.message_box("Telegram Error", f"Error joining channel: {str(e)}", type="error")
                return


            participants = await client.get_participants(self.group_name)

            for user in participants:
                if user.bot or user.deleted or not user.username:
                    continue

                self.logger.insert("end", f"@{user.username}\n")

