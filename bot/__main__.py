import uvloop
uvloop.install()

import logging
logging.basicConfig(format='%(asctime)s: %(lineno)d - %(levelname)s - %(message)s')
logging.getLogger().setLevel(logging.INFO)
logging.getLogger("pyrogram").setLevel(logging.WARNING)

from pyromod import listen 
from .config import Config
from pyrogram import Client
from .database import Database


class Bot(Client, Config):
    def __init__(self):
        super().__init__(
            "Acceptor",
            api_id=self.api_id,
            api_hash=self.api_hash,
            bot_token=self.bot_token,
            plugins=dict(root="bot/plugins"),
            workers=100,
            sleep_threshold=10
        )
        self.db = Database(self.database_url, 'approve')

    async def start(self):
        await super().start()
        self.me = await self.get_me()
        print(f"Bot Started at {self.me.first_name} ({self.me.username}).")
        print(" Now i am ready to accept new requests")

    async def stop(self, *args):
        await super().stop()
        print("Bot stopped. Bye.")


if __name__ == '__main__':
    Bot().run()