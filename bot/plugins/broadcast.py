from ..config import Config
from pyrogram import Client, filters
from helpers.broadcast import broadcast_handler


@Client.on_message(filters.private & filters.command("broadcast") & filters.user(Config.owner) & filters.reply)
async def _broadcast(client, message):
    await broadcast_handler(client, message)