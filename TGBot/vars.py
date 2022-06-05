import os
from dotenv import load_dotenv
load_dotenv()

class Var(object):
    API_ID=os.environ.get('API_ID', None)
    API_HASH=os.environ.get('API_HASH', None)
    BOT_TOKEN=os.environ.get('BOT_TOKEN', None)