import discord
import datetime
import os
import sys
import traceback
import helper

from discord.ext import commands

class owner(commands.Cog):
	"""Only owner can use these commands"""
	def __init__(self, bot):
		self.bot = bot

	@commands.command("all_data", description="Get someone videos data!")
	@commands.is_owner()
	async def _all_data(self, ctx):
		con=await helper.connect("db/channel.db")
		cur=await helper.cursor(con)
		await cur.execute("SELECT * FROM channel")
		print(await cur.fetchall())
		

	@commands.command("video_data", description="Get someone videos data!")
	@commands.is_owner()
	async def _video_data(self, ctx, ID):
		data=await helper.find_in_video(ID, mode='all')
		await ctx.send(f".{data}")

	@commands.command("data", description="Get someone channel data!")
	@commands.is_owner()
	async def _data(self, ctx, ID):
		data=await helper.find_in_channel(ID)
		await ctx.send(f".{data}")

	@commands.command("info_delete")
	@commands.is_owner()
	async def _info_delete(self, ctx):
		con=await helper.connect('db/channel.db')
		con2=await helper.connect('db/info.db')
		cur=await helper.cursor(con)
		cur2=await helper.cursor(con2)

		await cur.execute("DELETE FROM channel WHERE member_id = ?", (ctx.author.id,))
		await cur2.execute("DELETE FROM info WHERE member_id = ?", (ctx.author.id,))

		await con.commit()
		await con2.commit()
		await cur.close()
		await cur2.close()
		await con.close()
		await con2.close()
	
 
	@commands.command()
	@commands.is_owner()
	async def set_video(self, ctx):
		con=await helper.connect("db/video.db")
		cur=await helper.cursor(con)


		await cur.execute("UPDATE video SET deleted  = ? WHERE ID = ?", ("n", "2628051190"))

		await con.commit()
		await cur.close()
		await con.close()


	@commands.command("ss", hidden=True)
	@commands.is_owner()
	@commands.is_nsfw()
	async def _screenshot(self, ctx, *,name: str):
		await ctx.send(embed=discord.Embed(
			color=discord.Color.orange()
		).set_image(
			url=f"https://image.thum.io/get/width/3000/height/3000/http://www.{name}.com/"
		))


	@commands.command("reboot", description= "Restart the entire bot", aliases = ["restart"])
	@commands.is_owner()
	async def _reboot(self, ctx):
		try:
			if self.bot.processing_commands > 1:
				await ctx.send("I cant reboot right now because someone still using my command!")
				return

			await ctx.send(f"Rebooting: Im Online ;) {ctx.author.mention} in 3 seconds")
			await self.bot.close()
			os.execv(sys.executable, ["python"] + sys.argv)
		except Exception as e:
			tb = "".join(traceback.format_exception(type(e), e, e.__traceback__))
			await ctx.send(f"```py\n{tb}\n```")


		
	@commands.command('reload', description="Reload an extension", aliases=['re'])
	@commands.is_owner()
	async def _reload(self, ctx, *,filename: str):
		try:
			await ctx.send(embed=discord.Embed(
				title="Be Right Back!",
				description="Ok, Reloading...",
				color=discord.Color.blurple()
			))
			time_=datetime.datetime.utcnow()
			if filename == 'all':
				for fn in os.listdir("./cogs"):
					if fn.endswith(".py"):
						print("Reloaded: ", fn)
						self.bot.reload_extension(f'cogs.{fn[:-3]}')
				
				self.bot.reload_extension("jishaku")
				await ctx.send(embed=discord.Embed(
					title="Succesful",
					description=f"Succesfuly reloaded **All** cogs\nTook me `{datetime.datetime.utcnow() - time_}` to reloaded **ALL** cogs!",
					color=discord.Color.blurple()
				))

			else:
				self.bot.reload_extension(f"cogs.{filename}")
				await ctx.send(embed=discord.Embed(
					title="Succesful",
					description=f"Succesfuly reloaded {filename}.py\nTook me `{datetime.datetime.utcnow() - time_}` to reloaded!",
					color=discord.Color.blurple()
				))
		except Exception as e:
			tb = "".join(traceback.format_exception(type(e), e, e.__traceback__))
			await ctx.send(embed=discord.Embed(
				title="An Error Has Occured",
				description=f"```py\n{tb}\n```",
				color=discord.Color.red()
			))

def setup(bot):
	bot.add_cog(owner(bot))