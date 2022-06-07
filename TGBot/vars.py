import os
from dotenv import load_dotenv
load_dotenv()

class Var(object):
    API_ID=os.environ.get('API_ID', None)
    API_HASH=os.environ.get('API_HASH', None)
    BOT_TOKEN=os.environ.get('BOT_TOKEN', None)
    PORT=os.environ.get('PORT', 8080)
    if "DYNO" in os.environ:
        ON_HEROKU = True
        APP_NAME = str(os.environ.get("APP_NAME"))
    else:
        ON_HEROKU = False
    WORKERS=int(os.environ.get('WORKERS', 4))