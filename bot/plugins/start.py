import logging
log = logging.getLogger(__name__)
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
@Client.on_message(filters.command("start") & filters.private & filters.incoming)
async def start(client, message):
    try:
        start_buttons = [[
                 InlineKeyboardButton('JugaadLife™- Never pay full🛍️', url='https://t.me/+Mc_rMtgzQrgzNGJl'),
            ]
        ]
        markup = InlineKeyboardMarkup(start_buttons)
        await message.reply(
           
            f'''Add This 🤖Bot To Your Channel or Group To Accept Join Requests Automatically 😊\n\n**Features**👇\n\n🗣Custom welcome messages\n\n🗣Ads free BOT\n\nAdd Your Channel by pressing 

/add_channel -100xxxxxxxx''',


            reply_markup=markup,
            quote=True
        )
    except Exception as e:
        log.exception(e)
