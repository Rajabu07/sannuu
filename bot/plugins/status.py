import shutil, psutil
from ..config import Config
from pyrogram import Client, filters
from helpers.humanbytes import humanbytes


@Client.on_message(filters.private & filters.command("users") & filters.user(Config.owner))
async def show_status_count(client, message):
    total, used, free = (humanbytes(x) for x in shutil.disk_usage("."))
    cpu_usage = psutil.cpu_percent()
    ram_usage = psutil.virtual_memory().percent
    disk_usage = psutil.disk_usage('/').percent
    total_users = await client.db.total_users_count()
    
    text = f"Total Disk Space: {total} \n"
    text += f"Used Space: {used}({disk_usage}%) \n"
    text += f"Free Space: {free} \n"
    text += f"CPU Usage: {cpu_usage}% \n"
    text += f"RAM Usage: {ram_usage}%\n\n"
    text += f"Total Users : {total_users}"

    await message.reply(text=text, quote=True)