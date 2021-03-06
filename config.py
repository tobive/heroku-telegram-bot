# config.py
# this module took variables from env
from os.path import join, dirname
from os import environ
from dotenv import load_dotenv

dotenv_path = join(dirname(__file__),'.env')
load_dotenv(dotenv_path)

BOT_TOKEN = environ.get('BOT_TOKEN')
MONGOLAB_URI = environ.get('MONGOLAB_URI')
WEBHOOK = environ.get('WEBHOOK')
