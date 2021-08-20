import discord
import datetime
import os
import sys
import traceback

from discord.ext import commands

class owner(commands.Cog):
	"""Only owner can use these commands"""
	def __init__(self, bot):
		self.bot = bot


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
			channel=ctx.channel
			await ctx.send("Rebooting")
			await channel.send(f"Im Online ;) {ctx.author.mention} in 3 seconds")
			await self.bot.close()
			os.execv(sys.executable, ["python"] + sys.argv)
		except Exception as e:
			tb = "".join(traceback.format_exception(type(e), e, e.__traceback__))
			await ctx.send(f"```py\n{tb}\n```")

	@commands.command('logout', description="Shutdown the entire bot system", aliases=['shutdown'])
	@commands.is_owner()
	async def _logout(self, ctx):
		await ctx.send(embed=discord.Embed(
			description="Logging out...",
			color=discord.Color.blurple()
		))
		await self.bot.close()
		
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