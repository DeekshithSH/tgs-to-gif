import asyncio
import os
import secrets
import time
import traceback

from pyrogram import Client, filters
from pyrogram.types import Message
from TGBot.bot import Bot

@Bot.on_message(filters.sticker & filters.private)
async def sticker_handler(b, m: Message):
    try:
        file_name = m.sticker.file_name
        workdir=str(os.getcwd())+"/downloads/"+str(m.from_user.id)+str(int(time.time()))+str(secrets.token_hex(2))
        file_name2=workdir+"/"+file_name

        edit_msg=await m.reply_text('Processing', quote=True)

        await m.download(file_name2)

        process = await asyncio.create_subprocess_exec(
        *['tgs_to_gif', file_name2])
        await process.wait()
        print(process)

        await m.reply_animation(str(file_name2+".gif"), quote=True)
        await edit_msg.delete()
        os.remove(file_name2)
        os.remove(str(file_name2+".gif"))
        os.rmdir(workdir)
    except Exception as e:
        print(traceback.format_exc())
        await edit_msg.edit_text(f'error: {e}')
        try:
            os.remove(file_name2)
            os.remove(str(file_name2+".gif"))
            os.rmdir(workdir)
        except Exception as es:
            await m.reply_text(es, quote=True)