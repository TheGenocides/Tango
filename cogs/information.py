import discord
from dislash import ActionRow, Button, ButtonStyle, SelectMenu, SelectOption
from discord.ext import commands
import datetime

class information(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
		self.launch_time = datetime.datetime.utcnow()

	
	@commands.command("uptime", description="Show the bot uptime")
	async def _uptime(self, ctx):
		"""Show the bot uptime"""
		delta_uptime = datetime.datetime.utcnow() - self.launch_time
		hours, remainder = divmod(int(delta_uptime.total_seconds()), 3600)
		minutes, seconds = divmod(remainder, 60)
		days, hours = divmod(hours, 24)
		await ctx.send(embed=discord.Embed(
			description=f"**{days}D, {hours}H, {minutes}M, {seconds}S**",
			color=discord.Color.from_rgb(213, 240, 213)
		))

	@commands.command("news", description="Show a list of ideas for Tango bot in the future")
	async def _news(self, ctx):
		await ctx.send(embed=discord.Embed(
			title="Idea for the future",
			description="""
			**__Social Commands__**
			**•** p!info command for all info of a user
			**•** A report command if a video is breaking discord tos
			**•** Add unique ID to a video.
			**•** Make a bin command. Everytime a user deleted a video the video will get store in the bin.
			**•** Reupload command using Unique ID.
			
			
			**__Notification Commands__**\n
			**•** Youtube notif
			**•** FB notif
			**•** Instagram notif
			""",
			color=discord.Color.orange()
		).set_footer(
			text="• Last updated 8/11/2021"
		))

	@commands.command("info", description="Info for Tango bot")
	async def _info(self, ctx):
		await ctx.send(
			embed=discord.Embed(
				title="Tango Bot Stats",
				url="https://discord.com/api/oauth2/authorize?client_id=806725119917162527&permissions=242933428048&scope=applications.commands%20bot",
				color=discord.Color.from_rgb(213, 240, 213)
			).add_field(
				name="Servers",
				value=len(self.bot.guilds)
			).add_field(
				name="Users",
				value=len(self.bot.users)
			).add_field(
				name="prefix",
				value="`p!`"
			).add_field(
				name="Version",
				value="0.1.5"
			).add_field(
				name="Owner",
				value="TheGenofield#0110"
			).add_field(
				name="Age",
				value="I was made <t:1612383456:R>",
				inline=False
			))

			

def setup(bot):
	bot.add_cog(information(bot))