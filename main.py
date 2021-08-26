import bot
import os

from discord.ext import tasks
from dotenv import load_dotenv 
from dislash import InteractionClient

bot=bot.Tango()
bot.processing_commands = 0
slash=InteractionClient(bot)

@bot.before_invoke
async def before_invoke(ctx):
	bot.processing_commands += 1

@bot.after_invoke
async def after_invoke(ctx):
	bot.processing_commands -= 1

@tasks.loop(seconds=600)
async def _Database_backup():

load_dotenv()
os.environ["JISHAKU_NO_UNDERSCORE"] = "True"
os.environ["JISHAKU_RETAIN"] = "True"

_Database_backup.start()
bot._run_(os.environ["GAM"])