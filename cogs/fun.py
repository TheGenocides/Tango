import discord
import asyncio
import time
import humanize
import datetime
import helper

from dislash import ActionRow, Button, ButtonStyle
from discord.ext import commands


class Fun(commands.Cog):
	"""Fun Command for Tango bot"""
	def __init__(self, bot):
		self.bot = bot
		
		

	@commands.command("ping", description="Show the bot latency")
	async def _ping(self, ctx):
		"""Show the bot latency"""
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
		
	@commands.group()
	async def anime(self, ctx):
		await ctx.send_help()

	@anime.command("search")
	async def _search(self,ctx,  *,name):
		await ctx.send("Wait a sec :p")
		anime = helper.anime(name)

		msg=await ctx.send(embed=discord.Embed(
			description="**Select A Category!**",
			color=discord.Color.orange()
		),
			components=[
				ActionRow(
					Button(
						style=ButtonStyle.grey,
						label="Info",
						emoji="\U00002753",
						custom_id="info-button"
						
					),
					Button(
						style=ButtonStyle.grey,
						label="Episodes",
						emoji="\U0001f4fa",
						custom_id="episodes-button"
						
					),
					Button(
						style=ButtonStyle.grey,
						label="Miscellaneous ",
						emoji="\U00002699",
						custom_id="mis-button"
					)
				)
			]	
		)

		while True:
			inter=await ctx.wait_for_button_click(lambda inter: inter.author == ctx.author and inter.channel == ctx.channel)
			id_=inter.clicked_button.custom_id
			
			if id_ == "info-button":
				await msg.edit(embed=discord.Embed(
					title=anime[0],
					url=anime[1],
					description=anime[2],
					color=discord.Color.orange()
				).set_thumbnail(
					url=anime[3]
				),
					components=[
						ActionRow(
							Button(
								style=ButtonStyle.grey,
								label="Info",
								emoji="\U00002753",
								custom_id="info-button",
								disabled=True
								
							),
							Button(
								style=ButtonStyle.grey,
								label="Episodes",
								emoji="\U0001f4fa",
								custom_id="episodes-button"
								
							),
							Button(
								style=ButtonStyle.grey,
								label="Miscellaneous ",
								emoji="\U00002699",
								custom_id="mis-button"
							)
						)
					]	
				)

			elif id_ == "episodes-button":
				await msg.edit(embed=discord.Embed(
					title=anime[0],
					url=anime[1],
					color=discord.Color.orange()
				).set_thumbnail(
					url=anime[3]
				).add_field(
					name="📺 Episodes",
					value=anime[4]
				).add_field(
					name="🗃️ Genres",
					value=',\n'.join(anime[10])
				).add_field(
					name="<a:typingstatus:873477367522263081> Status",
					value=anime[12]
				).add_field(
					name="🌠 Teaser",
					value=f"[Click Me!]({anime[6]})"
				).add_field(
					name="🎬 Opening",
					value=anime[7]
				).add_field(
					name="🎬 Ending",
					value=anime[8]
				),
					components=[
						ActionRow(
							Button(
								style=ButtonStyle.grey,
								label="Info",
								emoji="\U00002753",
								custom_id="info-button"
							),
							Button(
								style=ButtonStyle.grey,
								label="Episodes",
								emoji="\U0001f4fa",
								custom_id="episodes-button",
								disabled=True
								
							),
							Button(
								style=ButtonStyle.grey,
								label="Miscellaneous ",
								emoji="\U00002699",
								custom_id="mis-button"
							)
						)
					]	
				)
			elif id_ == "mis-button":
				#15anime.producers
				await msg.edit(embed=discord.Embed(
					title=anime[0],
					url=anime[1],
					color=discord.Color.orange()
				).set_thumbnail(
					url=anime[3]
				).add_field(
					name="🏅 Ranked",
					value=anime[9]
				).add_field(
					name="🏅 Rating",
					value=anime[13]
				).add_field(
					name="⌛ Aired",
					value=anime[5]
				).add_field(
					name="<:Offline:873411447303057489> Type",
					value=anime[11]
				).add_field(
					name="🤩 Popularity",
					value=anime[14]
				).add_field(
					name="🎥 Producers",
					value=',\n'.join(anime[15]),
				),
					components=[
						ActionRow(
							Button(
								style=ButtonStyle.grey,
								label="Info",
								emoji="\U00002753",
								custom_id="info-button"
							),
							Button(
								style=ButtonStyle.grey,
								label="Episodes",
								emoji="\U0001f4fa",
								custom_id="episodes-button"
							),
							Button(
								style=ButtonStyle.grey,
								label="Miscellaneous ",
								emoji="\U00002699",
								custom_id="mis-button",
								disabled=True
							)
						)
					]	
				)
def setup(bot):
	bot.add_cog(Fun(bot))