import discord
import datetime
import os
import sys
import traceback
import helper
import aiohttp

from discord.ext import commands

class owner(commands.Cog):
	"""Only owner can use these commands"""
	def __init__(self, bot):
		self.bot = bot

	@commands.command("change")
	async def _change(self, ctx):
		con=await helper.connect("db/channel.db")
		cur=await helper.cursor(con)
		await cur.execute("SELECT * FROM channel WHERE member_id = ?", (637194463185469467,))
		await ctx.send(await cur.fetchone())


	@commands.command("verify_all")
	@commands.is_owner()
	async def _verify_all(self, ctx):
		con=await helper.connect("db/video.db")
		cur=await helper.cursor(con)
		await cur.execute("UPDATE video SET verified = ?", ("y",))
		await ctx.send("Verify all video!")
	
	@commands.command("verify")
	@commands.is_owner()
	async def _verify(self, ctx, ID):
		verified=self.bot.get_channel(884303044534206485)
		log=self.bot.get_channel(873919769122865162)
		data=await helper.find_in_video_by_id(ID, False)
		print(data)
		user=self.bot.get_user(data[0])
		print(data)
		if not data:
			await ctx.send("wrong id :/")
			return

		if data[16] == "y":
			await ctx.send("already verified!")
			return

		if not user:
			await ctx.send("Oh no cant find the user idk why. ask my dev to fix this error!")
			return

		if data[13] == "y":
			await ctx.send("Deleted video cant get verified!")
			return

		con=await helper.connect("db/video.db")
		cur=await helper.cursor(con)
		await cur.execute("UPDATE video SET verified = ? WHERE ID = ?", ('y', str(ID)))
		await con.commit()
		await cur.close()
		await con.close()
		await ctx.send(f"verified video with `{ID}` as its ID. I will dm the user to announce the news!")
		await user.send(f"We have verified your video! with `{ID}` has its ID! Thanks for using TangoBot!")
		await log.send(
			user.mention,
			embed=discord.Embed(
				title="Verified Video!",
				description=f"{user.mention} We have verified your video with `{ID}` as its ID!",
				color=self.bot.color[0]
			)
		)
		 

	@commands.command("decline")
	@commands.is_owner()
	async def _decline(self, ctx, ID, *,reason):
		verified=self.bot.get_channel(884303044534206485)
		log=self.bot.get_channel(873919769122865162)
		data=await helper.find_in_video_by_id(ID, False)
		
		if not data:
			await ctx.send("wrong id or the video already got decline/delete permanently! :/")
			return

		user=self.bot.get_user(int(data[0]))
		if not user:
			await ctx.send("Oh no cant find the user idk why. ask my dev to fix this error!")
			return

		con=await helper.connect("db/video.db")
		cur=await helper.cursor(con)
		await cur.execute("DELETE FROM video WHERE ID = ?", (ID,))
		await con.commit()
		await cur.close()
		await con.close()
		await ctx.send(f"Declined video with `{ID}` as its ID. I will dm the user to announce the news")
		await user.send(f"We have Declined your video because {reason}! With {ID} as its id.")
		await log.send(
			user.mention,
			embed=discord.Embed(
				title="Declined Video!",
				description=f"{user.mention} We have Declined your video because `{reason}`. With `{ID}` as its ID!",
				color=self.bot.color[1]
			).set_footer(
				text=f"If you want to appeal the problem you can DM {ctx.author}",
				icon_url=ctx.author.avatar_url
			).set_author(
				name=f"Declined By {ctx.author}",
				icon_url=ctx.author.avatar_url
			)
		)
		
		

	@commands.command("delete_account")
	@commands.is_owner()
	async def _delete_account(self, ctx, ID:int):
		con=await helper.connect('db/channel.db')
		con2=await helper.connect('db/info.db')
		con3=await helper.connect('db/video.db')
		con4=await helper.connect('db/comment.db')

		cur=await helper.cursor(con)
		cur2=await helper.cursor(con2)
		cur3=await helper.cursor(con3)
		cur4=await helper.cursor(con4)

		await cur.execute("DELETE FROM channel WHERE member_id = ?", (ID,))
		await cur2.execute("DELETE FROM info WHERE member_id = ?", (ID,))
		await cur3.execute("DELETE FROM video WHERE member_id = ?", (ID,))
		await cur4.execute("DELETE FROM comments WHERE commenter_id = ?", (ID,))

		await con.commit()
		await con2.commit()
		await con3.commit()
		await con4.commit()
		await cur.close()
		await cur2.close()
		await cur3.close()
		await cur4.close()
		await con.close()
		await con2.close()
		await con3.close()
		await con4.close()
		await ctx.send("Done!")

	# @commands.command("ss", hidden=True)
	# @commands.is_owner()
	# @commands.is_nsfw()
	# async def _screenshot(self, ctx, *,name: str):
	# 	await ctx.send(embed=discord.Embed(
	# 		color=discord.Color.from_rgb(136, 223 ,251)
	# 	).set_image(
	# 		url=f"https://image.thum.io/get/width/3000/height/3000/http://www.{name}.com/"
	# 	))


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
					title="Successful",
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

	@commands.command("fetch_channel")
	@commands.is_owner()
	async def _fetch_channel(self, ctx, ID):
		channel=await helper.find_in_channel(ID)
		if not channel:
			await ctx.send("no channel found")
		await ctx.send(channel)

def setup(bot):
	bot.add_cog(owner(bot))