import logging
log = logging.getLogger(__name__)

import asyncio
from ..config import Config
from pyrogram import Client, filters
from pyrogram.errors import UserAlreadyParticipant, UserIsBlocked, PeerIdInvalid, FloodWait
from helpers.str_to_buttons import string_to_buttons


@Client.on_chat_join_request()
async def approver(client, joinRequest):
    try:
        await client.approve_chat_join_request(joinRequest.chat.id, joinRequest.from_user.id)
    except (UserAlreadyParticipant, UserIsBlocked, PeerIdInvalid):
        pass
    except FloodWait as e:
        log.warning(f'Flood Wait, waiting for {e.value} sec')
        await asyncio.sleep(e.value+1)
        return await approver(client, joinRequest)
    except Exception as e:
        log.exception(e)
    else:
        try:
            user  = await client.db.is_user_exist(joinRequest.from_user.id)
            if not user:
                await client.db.add_user(joinRequest.from_user.id)
                if Config.log_channel:
                    try:
                        await client.send_message(
                            int(Config.log_channel),
                            f"""#NEW_USER: 

{joinRequest.from_user.mention} started

@{client.me.username} 😊"""
                        )
                    except Exception as e:
                        log.error(e)

            welcome_text, buttons = await client.db.get_welcome(joinRequest.chat.id)
            markup = await string_to_buttons(buttons)

            await client.send_message(
                joinRequest.from_user.id,
                text=welcome_text.replace('{name}', joinRequest.from_user.first_name).replace('{chat}', joinRequest.chat.title),
                reply_markup=markup
            )
        except (PeerIdInvalid, UserIsBlocked):
            pass
        except FloodWait as e:
            log.warning(f'Flood Wait for {e.value} sec')
            await asyncio.sleep(e.value)
        except Exception as e:
            log.error(e)
