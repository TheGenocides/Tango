import bot
import os

from dotenv import load_dotenv 

bot=bot.Tango()
bot.processing_commands = 0

@bot.before_invoke
async def before_invoke(ctx):
	bot.processing_commands += 1

@bot.after_invoke
async def after_invoke(ctx):
	bot.processing_commands -= 1



load_dotenv()
os.environ["JISHAKU_NO_UNDERSCORE"] = "True"
os.environ["JISHAKU_RETAIN"] = "True"

bot._run_(os.environ["GAM"])