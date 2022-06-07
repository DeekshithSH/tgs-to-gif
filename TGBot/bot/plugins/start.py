from pyrogram import Client, filters
from pyrogram.types import Message
from TGBot.bot import Bot

@Bot.on_message(filters.private & filters.command('start'))
async def start(b: Client, m: Message):
    await m.reply_text('Send me tgs Sticker')