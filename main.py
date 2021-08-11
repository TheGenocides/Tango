import bot
import os

from dotenv import load_dotenv 
from dislash import SlashClient

client=bot.Tango()
slash=SlashClient(client)

load_dotenv()
os.environ["JISHAKU_NO_UNDERSCORE"] = "True"
os.environ["JISHAKU_RETAIN"] = "True"

client._run_(os.environ["GAM"])