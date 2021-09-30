import discord
import functools
import helper
from discordTogether import DiscordTogether

from dislash import ActionRow, Button, ButtonStyle
from discord.ext import commands
from easy_pil import Editor

class fun(commands.Cog):
	"""Fun Command for Tango bot"""
	def __init__(self, bot):
		self.bot = bot
		self.game = DiscordTogether(self.bot)
	
	@commands.command("bar", description="Percentage the number given and turn it into bar similar to exp bar")
	async def _bar(self, ctx, number):
		try:
			number=float(number) if not isinstance(number, int) else int(number)  
		except Exception as e:
			await ctx.send("Number must be a number not letters!")
			raise e
			return			

		def make_card(self):  #40, 436
			bg=Editor("assets/bg.png")    #650        #40
			bg.rectangle((40, 550), width=1190, height=50, fill="white", radius=20)
			bg.bar((40, 550), max_width=1190, height=50, percentage=(100/100)*number, fill="#5bfa9e", radius=20)
			return bg.image_bytes
		
		raw=functools.partial(make_card, self)
		card=await self.bot.loop.run_in_executor(None, raw)
		await ctx.send(file=discord.File(fp=card, filename="card.png"))


	
	@commands.command('leave', description="Make me leave this guild :(")
	@commands.has_permissions(kick_members=True)
	async def _leave(self, ctx):
		await ctx.send("Byee :(")
		await ctx.guild.leave()

	@commands.group(invoked_without_command=True)
	@commands.cooldown(1, 7, commands.BucketType.user)
	async def anime(self, ctx):
		pass
	
	@anime.command("lyric", description="Get info about anime lyric!")
	@commands.cooldown(1, 7, commands.BucketType.user)
	async def _lyric(self, ctx, *,name):
		try:
			msg=await ctx.send("Fetching Data...")
			lyric = functools.partial(helper.lyric, name)
			lyric = await self.bot.loop.run_in_executor(None, lyric)
			await msg.edit(content="Found it!")

			msg=await ctx.send(embed=discord.Embed(
				description="**Select The Language!**",
				color=discord.Color.orange()
			), components=[
				ActionRow(
					Button(
						style=ButtonStyle.green,
						label="English",
						custom_id="english" 
					),
					Button(
						style=ButtonStyle.green,
						label="Kanji",
						custom_id="kanji"
						
					),
					Button(
						style=ButtonStyle.green,
						label="Romaji",
						custom_id="romaji"
					),
					Button(
						style=ButtonStyle.red,
						label="Cancel",
						custom_id="abort"
					)
				)
			]
		)

		
			on_click=msg.create_click_listener(timeout=120)
			
			@on_click.not_from_user(ctx.author, cancel_others=True, reset_timeout=False)
			async def on_wrong_user(inter):
				await inter.reply(
					embed=discord.Embed(
					description="You are not the member who use this command!",
					color=discord.Color.red()
				), 
					ephemeral=True
				)

			@on_click.matching_id("english")
			async def _English(inter):
				await inter.reply(
					type=7,
					embed=discord.Embed(
					title="English Lyric",
					url=lyric[0],
					description=lyric[1],
					color=discord.Color.orange()
				),
					components=[
						ActionRow(
							Button(
								style=ButtonStyle.green,
								label="English",
								custom_id="english",
								disabled=True
								
							),
							Button(
								style=ButtonStyle.green,
								label="Kanji",
								custom_id="kanji"
								
							),
							Button(
								style=ButtonStyle.green,
								label="Romaji",
								custom_id="romaji"
							),
							Button(
								style=ButtonStyle.red,
								label="Cancel",
								custom_id="abort"
							)
						)
					]	
				)

			@on_click.matching_id("kanji")
			async def _Kanji(inter):
				await inter.reply(
					type=7,
					embed=discord.Embed(
					title="Kanji Lyric",
					url=lyric[0],
					description=lyric[2],
					color=discord.Color.orange()
				),
					components=[
						ActionRow(
							Button(
								style=ButtonStyle.green,
								label="English",
								custom_id="english"
							),
							Button(
								style=ButtonStyle.green,
								label="Kanji",
								custom_id="kanji",
								disabled=True
							),
							Button(
								style=ButtonStyle.green,
								label="Romaji",
								custom_id="romaji"
							),
							Button(
								style=ButtonStyle.red,
								label="Cancel",
								custom_id="abort"
							)
						)
					]	
				)

			@on_click.matching_id("romaji")
			async def _Romaji(inter):
				await inter.reply(
					type=7,
					embed=discord.Embed(
					title="Romaji Lyric",
					url=lyric[0],
					description=lyric[3],
					color=discord.Color.orange()
				),
					components=[
						ActionRow(
							Button(
								style=ButtonStyle.green,
								label="English",
								custom_id="english"
							),
							Button(
								style=ButtonStyle.green,
								label="Kanji",
								custom_id="kanji"
							),
							Button(
								style=ButtonStyle.green,
								label="Romaji",
								custom_id="romaji",
								disabled=True
							),
							Button(
								style=ButtonStyle.red,
								label="Cancel",
								custom_id="abort"
							)
						)
					]		
				)

			@on_click.timeout
			async def _on_timeout():
				await ctx.send("I have stop the command due to its long activity!")
				await msg.delete()

			@on_click.matching_id("abort")
			async def _abort(inter):
				await inter.message.delete()
				on_click.kill()

		except Exception as e:
			raise e
		
	@anime.command("search", description="Get info about anime stats and much more!")
	@commands.cooldown(1, 7, commands.BucketType.user)
	async def _search(self, ctx,  *,name):
		try:
			msg=await ctx.send("Fetching Data...")
			anime = functools.partial(helper.anime, name)
			anime = await self.bot.loop.run_in_executor(None, anime)

			if anime[16] and not ctx.channel.is_nsfw():
				await ctx.send("Looks like this anime is nsfw :/ make sure to use this command in nsfw channels!")
				return

			await msg.edit(content="Found it!")
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

		
			on_click=msg.create_click_listener(timeout=120)
			
			@on_click.not_from_user(ctx.author, cancel_others=True, reset_timeout=False)
			async def on_wrong_user(inter):
				await inter.reply(
					embed=discord.Embed(
					description="You are not the member who use this command!",
					color=discord.Color.red()
				), 
					ephemeral=True
				)

			@on_click.matching_id("info-button")
			async def _Info(inter):
				await inter.reply(
					type=7,
					embed=discord.Embed(
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

			@on_click.matching_id("episodes-button")
			async def _episodes_Button(inter):
				await inter.reply(
					type=7,
					embed=discord.Embed(
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
			@on_click.matching_id("mis-button")
			async def _mis_button(inter):
				await inter.reply(
					type=7,
					embed=discord.Embed(
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

		except AttributeError:
			await msg.edit(content=f"No anime called `{name}`. Make sure to type it properly")

	@commands.command("watch", description="Watch youtube with your friend!")
	async def _watch(self, ctx, player=3, time=100):
		if not ctx.author.voice:
			await ctx.send("You must connect to a voice channel first!")
			return

		link = await self.game.create_link(ctx.author.voice.channel.id, 'youtube', max_age=time, max_uses=player)
		await ctx.send(f"**Youtube Together!**\n**`Host > Click the Link`**\n**`Player > Click the play button, you do need to wait till the host click the blue link!`**\n**`Spectator > Click the spectate button`**\nlink ---> {link}")

	@commands.command("chess", description="play a game of chess with your friend!")
	async def _chess(self, ctx, player=3, time=100):
		if not ctx.author.voice:
			await ctx.send("You must connect to a voice channel first!")
			return

		link = await self.game.create_link(ctx.author.voice.channel.id, 'chess', max_age=time, max_uses=player)
		await ctx.send(f"**Chess Together!**\n**`Host > Click the Link`**\n**`Player > Click the play button, you do need to wait till the host click the blue link!`**\n**`Spectator > Click the spectate button`**\nlink ---> {link}")

	@commands.command("fishing", aliases=['fish'], description="play a game of fishing with your friend!")
	async def _fishing(self, ctx, player=3, time=100):
		if not ctx.author.voice:
			await ctx.send("You must connect to a voice channel first!")
			return

		link = await self.game.create_link(ctx.author.voice.channel.id, 'betrayal', max_age=time, max_uses=player)
		await ctx.send(f"**Fishing Together!**\n**`Host > Click the Link`**\n**`Player > Click the play button, you do need to wait till the host click the blue link!`**\n**`Spectator > Click the spectate button`**\nlink ---> {link}")	

	@commands.command("betrayal", aliases=['betray'], description="play a game of betrayal with your friend!")
	async def _betrayal(self, ctx, player=3, time=100):
		if not ctx.author.voice:
			await ctx.send("You must connect to a voice channel first!")
			return

		link = await self.game.create_link(ctx.author.voice.channel.id, 'betrayal', max_age=time, max_uses=player)
		await ctx.send(f"**Betrayal Together!**\n**`Host > Click the Link`**\n**`Player > Click the play button, you do need to wait till the host click the blue link!`**\n**`Spectator > Click the spectate button`**\nlink ---> {link}")	


	@commands.command("poker",  description="play a game of poker with your friend!")
	async def _poker(self, ctx, player=3, time=100):
		if not ctx.author.voice:
			await ctx.send("You must connect to a voice channel first!")
			return

		link = await self.game.create_link(ctx.author.voice.channel.id, 'poker', max_age=time, max_uses=player)
		await ctx.send(f"**Poker Together!**\n**`Host > Click the Link`**\n**`Player > Click the play button, you do need to wait till the host click the blue link!`**\n**`Spectator > Click the spectate button`**\nlink ---> {link}")	

 	
def setup(bot):
	bot.add_cog(fun(bot))