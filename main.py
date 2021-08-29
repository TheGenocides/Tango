import bot
import os
import helper
import asyncio
import aiohttp

from discord.ext import tasks
from dotenv import load_dotenv 

bot=bot.Tango()
bot.processing_commands = 0

@bot.before_invoke
async def before_invoke(ctx):
	bot.processing_commands += 1

@bot.after_invoke
async def after_invoke(ctx):
	bot.processing_commands -= 1

@tasks.loop(seconds=600)
async def _Database_backup(): 
	os.system('git add db')
	os.system(f"git commit -m 'Database Backup from _Database_backup'")
	print("I have commited a git")
	
@tasks.loop(seconds=1800)
async def _Clear_history(): 
	try:
		await asyncio.sleep(120)
		con=await helper.connect("db/info.db")
		cur=await helper.cursor(con)
	
		await cur.execute("UPDATE info SET viewed = ?", ("[]",))
		await con.commit()
		await cur.close()
		await con.close()
		print("I have clear history of all users!")
	except Exception as e:
		raise e

@tasks.loop(seconds=5000)
async def _Change_server_Count():
	async with aiohttp.ClientSession() as session:
		url="https://disbotlist.xyz/api/bots/stats"
		headers={"ServerCount": str(len(bot.guilds)), "Authorization": os.environ['dbl']}
		async with session.post(url, headers=headers) as response:
			pass

load_dotenv()
os.environ["JISHAKU_NO_UNDERSCORE"] = "True"
os.environ["JISHAKU_RETAIN"] = "True"

_Database_backup.start()
_Clear_history.start()
_Change_server_Count.start()
bot._run_(os.environ["GAM"])