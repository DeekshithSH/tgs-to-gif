import asyncio
import logging
import sys
import glob
import importlib
from aiohttp import web
from pathlib import Path
from pyrogram import idle
from TGBot.server import web_server
from TGBot.bot import Bot
from TGBot.utils.keep_alive import ping_server
from TGBot.vars import Var

#logging
logging.basicConfig(
    level=logging.INFO,
    datefmt="%d/%m/%Y %H:%M:%S",
    format='[%(asctime)s] {%(pathname)s:%(lineno)d} %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler(stream=sys.stdout),
              logging.FileHandler("bot.log", mode="a", encoding="utf-8")],)

logging.getLogger("aiohttp").setLevel(logging.ERROR)
logging.getLogger("pyrogram").setLevel(logging.ERROR)
logging.getLogger("aiohttp.web").setLevel(logging.ERROR)

server = web.AppRunner(web_server())

path = "TGBot/bot/plugins/*.py"
files = glob.glob(path)

loop=asyncio.get_event_loop()

async def main():
    print('------------------- Importing -------------------')
    for name in files:
        with open(name) as a:
            patt = Path(a.name)
            plugin_name = patt.stem.replace(".py", "")
            plugins_dir = Path(f"TGBot/bot/plugins/{plugin_name}.py")
            import_path = ".plugins.{}".format(plugin_name)
            spec = importlib.util.spec_from_file_location(import_path, plugins_dir)
            load = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(load)
            sys.modules["TGBot.bot.plugins." + plugin_name] = load
            print("Imported => " + plugin_name)
    print('Starting Bot')
    await Bot.start()
    bot_info=await Bot.get_me()
    Bot.username=bot_info.username
    print('Done')
    if Var.ON_HEROKU:
        print("Starting Keep Alive Service")
        print()
        asyncio.create_task(ping_server())
    print("Initalizing Web Server")
    await server.setup()
    bind_address = "0.0.0.0"
    await web.TCPSite(server, bind_address, Var.PORT).start()
    print("Done")
    await idle()

try:
    loop.run_until_complete(main())
except Exception as e:
    logging.error(e)