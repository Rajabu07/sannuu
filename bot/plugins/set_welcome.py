import logging
log = logging.getLogger(__name__)

from pyrogram import Client, filters, enums
from helpers.str_to_buttons import string_to_buttons
from pyrogram.errors import (
    ChatAdminRequired, UserNotParticipant,
    ChannelPrivate, ChannelInvalid,
    ChatInvalid, PeerIdInvalid
)


@Client.on_message(filters.command('set_welcome'))
async def set_welcome(client, message):
    text = '''**Please Follow the following steps to Set Welcome**

>> Add bot to your group or channel and make it as admin.
>> Add Your Group or Channel by Sending /add_channel -100xxxxxx. 
>> Folow the On Screen instructions
'''
    await message.reply(text=text, quote=True)


@Client.on_message(filters.command('add_channel'))
async def get_channel(client, message):
    not_correct_format = '''**Please Follow the following steps to Add Channel**

>> Add bot to your group or channel and make it as admin.
>> Now send your channel id in below format
        
/add_channel -100xxxxxx.\n(to Get Channel Id Forward any Message to @chat_id_echo_bot From Your Channel)'''

    if len(message.command) == 2:
        try:
            channel_id = int(message.command[1])
        except:
            text = not_correct_format
        else:
            try:
                user = await client.get_chat_member(channel_id, message.from_user.id)
                if user.status in [enums.ChatMemberStatus.OWNER, enums.ChatMemberStatus.ADMINISTRATOR]: 
                    text = "Enter the welcome message you want the new approved members to receive.\n\n"
                    text += "Available formattings:\n"
                    text += "- `{name}` - users name.\n"
                    text += "- `{chat}` - chat title.\n"
                    welcome = await message.chat.ask(text)
                    text = "Now send the button to be added in the format show below. "
                    text += "Use /pass if you dont want to add buttons\n\n"
                    text += "For adding buttons in same row\n"
                    text += "`button1 - https://t.me/ | button2 - https://t.me/`\n\n"
                    text += "For adding buttons in different rows\n"
                    text += "`button1 - https://t.me/ \n button2 - https://t.me/`\n\n"
                    buttons = await message.chat.ask(text)
                    try:
                        markup = await string_to_buttons(buttons.text)
                    except Exception as e:
                        log.error(e)
                        buttons.text = markup = None
                    await client.db.update_welcome(channel_id, welcome.text, buttons.text)
                    welcome_msg = await message.reply(welcome.text, reply_markup=markup)
                    return await welcome_msg.reply("From now this message will be send when an user was auto approved.", quote=True)
                else:
                    text = "You are not the admin of that chat so i don't allow you to do that." 
            except (ChatAdminRequired, UserNotParticipant, ChannelPrivate, ChannelInvalid, ChatInvalid, PeerIdInvalid):
                text = "You haven't made me as an admin in your group or channel. Please make me admin and try again later."
            except Exception as e:
                log.exception(e)
                text = "Something went wrong"
    else:
        text = not_correct_format
    await message.reply(text, quote=True)