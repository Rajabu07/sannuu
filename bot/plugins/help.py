from pyrogram import Client, filters


@Client.on_message(filters.command('help') & filters.private & filters.incoming)
async def help(client, message):
    text = '''**Please Follow the following steps to Use This Bot**

>> Add bot to your group or channel and make it as admin.
>> Add Your Group or Channel by Sending /add_channel -100xxxxxx. 
>> Folow the On Screen instructions
'''
    await message.reply(text, quote=True)
