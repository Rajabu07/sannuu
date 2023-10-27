import io
import time
import string
import random
import asyncio
import datetime
import traceback
from pyrogram.types import Message
from pyrogram.errors import FloodWait, InputUserDeactivated, UserIsBlocked, PeerIdInvalid

broadcast_ids = {}

async def send_msg(user_id, message):
    try:
        msg = await message.copy(chat_id=user_id)
        return 200, msg
    except FloodWait as e:
        await asyncio.sleep(e.value)
        return await send_msg(user_id, message)
    except InputUserDeactivated:
        return 400, f"{user_id} : deactivated\n"
    except UserIsBlocked:
        return 400, f"{user_id} : blocked the bot\n"
    except PeerIdInvalid:
        return 400, f"{user_id} : user id invalid\n"
    except Exception as e:
        return 500, f"{user_id} : {traceback.format_exc()}\n"


async def broadcast_handler(c, m):
    all_users = await c.db.get_all_users()
    broadcast_msg = m.reply_to_message
    while True:
        broadcast_id = ''.join([random.choice(string.ascii_letters) for i in range(3)])
        if not broadcast_ids.get(broadcast_id):
            break
    out = await m.reply_text(
        text=f"Broadcast Started! You will be notified with log file when all the users are notified 😊"
    )
    start_time = time.time()
    total_users = await c.db.total_users_count()
    done = 0
    failed = 0
    success = 0
    broadcast_ids[broadcast_id] = dict(
        total=total_users,
        current=done,
        failed=failed,
        success=success
    )
    log_file = io.BytesIO()
    log_file.name = f"{datetime.datetime.utcnow()}_broadcast.txt"
    broadcast_log = ""
    broadcast_messages = []
    async for user in all_users:
        sts, msg = await send_msg(
            user_id=int(user['id']),
            message=broadcast_msg
        )
        if sts == 200:
            success += 1
            broadcast_messages.append(msg)
        else:
            failed += 1
            broadcast_log += msg
        #if sts == 400:
            #await c.db.delete_user(user['id'])
        done += 1
        if broadcast_ids.get(broadcast_id) is None:
            break
        else:
            broadcast_ids[broadcast_id].update(
                dict(
                    current=done,
                    failed=failed,
                    success=success
                )
            )
    if broadcast_ids.get(broadcast_id):
        broadcast_ids.pop(broadcast_id)
    completed_in = datetime.timedelta(seconds=int(time.time() - start_time))
    await asyncio.sleep(0.5)
    await out.delete()
    log_file.write(broadcast_log.encode())
    if failed == 0:
        await m.reply_text(
            f"broadcast completed in `{completed_in}`\n\nTotal users {total_users}.\nTotal done {done}, {success} success and {failed} failed.",
            quote=True
        )
    else:
        await m.reply_document(
            document=log_file,
            caption=f"broadcast completed in `{completed_in}`\n\nTotal users {total_users}.\nTotal done {done}, {success} success and {failed} failed.",
        )
    
    await asyncio.sleep(8*60*60) # sleping for hours
    for msg in broadcast_messages:
        try:
            await msg.delete()
            await asyncio.sleep(0.5)
        except FloodWait as e:
            await asyncio.sleep(e.value+1)
            await msg.delete()
        except:
            pass 