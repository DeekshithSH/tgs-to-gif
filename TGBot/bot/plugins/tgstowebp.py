import os
import secrets
import time

from pyrogram import Client, filters
from pyrogram.types import Message
from TGBot.bot import Bot

from lottie.exporters import exporters
from lottie.importers import importers

@Bot.on_message(filters.sticker & filters.private)
async def sticker_handler(b, m: Message):
    try:
        start_time=time.time()
        file_name = m.sticker.file_name
        workdir=str(os.getcwd())+"/downloads/"+str(m.from_user.id)+str(int(time.time()))+str(secrets.token_hex(2))
        file_name2=workdir+"/"+file_name

        edit_msg=await m.reply_text('Processing', quote=True)

        await m.download(file_name2)
        await edit_msg.edit_text(f'Converting to gif | {(time.time()) - start_time}')

        importer = None
        suf = os.path.splitext(file_name2)[1][1:]

        for p in importers:
            if suf in p.extensions:
                importer = p
                break

        outfile = os.path.splitext(file_name2)[0]+'.gif'
        if not outfile:
            outfile = os.path.splitext(file_name2)[0]+'.gif'
        exporter = exporters.get_from_filename(outfile)
    
        an = importer.process(file_name2)

        exporter.process(an, outfile)
        await edit_msg.edit_text(f'Uploading | {(time.time()) - start_time}')
        start_time=time.time()
        await m.reply_animation(outfile, quote=True)
        
        os.remove(file_name2)
        os.remove(outfile)
        os.rmdir(workdir)
        await edit_msg.edit_text(f'Done | {(time.time()) - start_time}')
    except Exception as e:
        await edit_msg.edit_text(f'error: {e} | {(time.time()) - start_time}')
        try:
            os.remove(file_name2)
            os.remove(outfile)
            os.rmdir(workdir)
        except Exception as es:
            await m.reply_text(es, quote=True)