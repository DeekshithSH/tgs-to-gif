import asyncio
import logging
import sys
import glob
import importlib
from pathlib import Path
from pyrogram import idle
from TGBot.bot import Bot

#logging
logging.basicConfig(
    level=logging.INFO,
    datefmt="%d/%m/%Y %H:%M:%S",
    format='[%(asctime)s] {%(pathname)s:%(lineno)d} %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler(stream=sys.stdout),
              logging.FileHandler("bot.log", mode="a", encoding="utf-8")],)

logging.getLogger("pyrogram").setLevel(logging.ERROR)

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
    print('Done')
    await idle()

try:
    loop.run_until_complete(main())
except Exception as e:
    logging.error(e)