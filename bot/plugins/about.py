from pyrogram import Client, filters


@Client.on_message(filters.command('about') & filters.private & filters.incoming)
async def about(client, message):
    text = '''**Hello I'm  Auto Approve Join Request Bot**

I'm a Simple Telegram Bot to Approve Join Request Automatically, 

You Can also Set a Custom Welcome Message. 

**I'm 100% Ads Free**😊 
'''
    await message.reply(text, quote=True)
