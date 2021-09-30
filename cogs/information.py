import discord
import humanize
import datetime
import asyncio
import time

from dislash import ActionRow, Button, ButtonStyle, SelectMenu, SelectOption
from discord.ext import commands

class information(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
		self.launch_time = datetime.datetime.utcnow()

	@commands.command("uptime", description="Show the bot uptime")
	@commands.cooldown(1, 3, commands.BucketType.user)
	async def _uptime(self, ctx):
		delta_uptime = datetime.datetime.utcnow() - self.launch_time
		hours, remainder = divmod(int(delta_uptime.total_seconds()), 3600)
		minutes, seconds = divmod(remainder, 60)
		days, hours = divmod(hours, 24)
		await ctx.send(embed=discord.Embed(
			description=f"**{days}D, {hours}H, {minutes}M, {seconds}S**",
			color=discord.Color.from_rgb(213, 240, 213)
		))

	@commands.command("news", description="Show a list of ideas for Tango bot in the future")
	@commands.cooldown(1, 3, commands.BucketType.user)
	async def _news(self, ctx):
		await ctx.send(embed=discord.Embed(
			description="""**#0 TangoNews! <t:1629810506:R>**
Howdy folks, Welcome to TangoNews where you can get the latest news about Tango bot!

**1. TangoNews** <:Tango:878902180856352848> 
This is the first ever TangoNews series!! I will try to include minimum of 3 news every 2 weeks! So wait till the 7 of September for the next series!

**2. Lockdown** <:blurplelock:879722735725596702> 
TangoBot when on a lockdown for 2 days! Why? because TangoBot's db got malformed and I believe TangoBot has many error and i need to fix it before i open TangoBot again! 

**3. Update 0.1.7** <:announcement:875659362109124629> 
TangoBot will get an update to version 0.1.7, we still don't know when exactly but its definitely before September! New feature include: comment system, more bugs fixed. Added new command like delete video command, comment command, info command, vote command, edit video command, login & logout command(which use your email and password) and many more functions! I try to make more commands that can be useful for the community also since TangoBot is base on YouTube i will find inspiration there! 

Thats all for today folks!
See you next time!""",
			color=discord.Color.orange()
		).set_footer(
			text="• Last updated 8/27/2021"
		))
	@commands.command("ping", description="Show the bot latency")
	@commands.cooldown(1, 3, commands.BucketType.user)
	async def _ping(self, ctx):
		loading = "<a:DiscordSpin:795546311319355393>"
		ws_ping = f"{(self.bot.latency * 1000):.2f}ms " \
		f"({humanize.precisedelta(datetime.timedelta(seconds=self.bot.latency))})"
		embed=discord.Embed(
			title="PONG! :ping_pong:",
			description=f"**{loading} Websocket:** Calculating...\n**:repeat: Round-Trip:** Calculating...",
			color=discord.Color.orange()
		)
		start = time.perf_counter()
		message = await ctx.send(embed=embed)
		end = time.perf_counter()
		await asyncio.sleep(0.5)
		trip = end - start
		rt_ping = f"{(trip * 1000):.2f}ms ({humanize.precisedelta(datetime.timedelta(seconds=trip))})"
		embed.description = (
			f"**{loading} Websocket:** {ws_ping}\n**:repeat: Round-Trip:** {rt_ping}"
		)
		await message.edit(embed=embed)

	@commands.command("info", description="Info for Tango bot")
	@commands.cooldown(1, 5, commands.BucketType.user)
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

	@commands.command("vote", description="Get a link for voting TangoBot!")
	@commands.cooldown(1, 3, commands.BucketType.user)
	async def _vote(self, ctx):
		await ctx.send("Considering voting me on DBL list! https://disbotlist.xyz/bot/806725119917162527/")

	@commands.command("invite", description="Get a link for inviting TangoBot!")
	@commands.cooldown(1, 3, commands.BucketType.user)
	async def _invite(self, ctx):
		await ctx.send("You can invite me by clicking this link!\nhttps://discord.com/api/oauth2/authorize?client_id=806725119917162527&permissions=242933428048&scope=applications.commands%20bot")

	

def setup(bot):
	bot.add_cog(information(bot))