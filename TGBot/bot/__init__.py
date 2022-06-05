from pyrogram import Client
from TGBot.vars import Var

Bot=Client(
    name='TGBot',
    api_id=Var.API_ID,
    api_hash=Var.API_HASH,
    bot_token=Var.BOT_TOKEN,
    sleep_threshold=60,
    workdir="TGBot",
    plugins={"root": "TGBot/bot/plugins"},
    )