import loguru
from telethon import TelegramClient

from src.func import get_proxy_object


class Client:

    def __init__(self, path: str, api_id: int, api_hash: str, proxy: str) :
        self.api_id = api_id
        self.api_hash = api_hash
        self.session_path = path
        self.proxy = proxy

        self.client = TelegramClient(self.session_path, proxy=get_proxy_object(proxy), api_id=self.api_id, api_hash=self.api_hash, system_version="Windows 10")


    async def __aenter__(self):
        await self.client.connect()
        return self.client

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.client.disconnect()

    async def is_valid(self):
        try:
            async with self:
                return await self.client.is_user_authorized()
        except Exception as e:
            loguru.logger.error(e)
            return False



