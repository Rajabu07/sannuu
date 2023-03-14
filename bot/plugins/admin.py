from ..config import Config
from pyrogram import Client, filters

@Client.on_message(filters.private & filters.command("admin") & filters.user(Config.owner))
async def admin(client, message): 
    text = '''**Available Commands**\n
/broadcast - Reply to a message and use this command to send that message to all of the bot users.\n
/users - Shows the total no. of users of the bot\n
(Admin Message).'''

    await message.reply(text=text, quote=True)
