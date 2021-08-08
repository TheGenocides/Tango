import discord
import asyncio
import helper

#===============================

from discord.ext import commands
from dislash import ActionRow, Button, ButtonStyle, SelectMenu, SelectOption, SlashClient

class Social(commands.Cog):
	"""Social is a group of commands that contain most of the commands that other can use ;)"""
	def __init__(self, bot):
		self.bot = bot
		self.channel_error = discord.Embed(
			description="You havent make your channel yet, Use p!start command!",
			color=discord.Color.red()
		)

		self.video_error = discord.Embed(
			color=discord.Color.red()
		).set_footer(
			text="You havent a video yet, use p!post command!"
		)

		self.review=None

	@commands.command()
	async def start(self, ctx):
		db=await helper.connect("db/channel.db")
		db2=await helper.connect("db/info.db")
		cur=await helper.cursor(db)	
		cur2=await helper.cursor(db2) 
		await cur.execute("SELECT member_id FROM channel WHERE member_id=?", (int(ctx.author.id),))
		print(await cur.fetchone())

		await ctx.send(embed=discord.Embed(
			title="Time to get start!!",
			description="Hello There 👋\nTo create your channel you need to follow this 3 steps\n\n**1.** Choose your channel name! (Can get change later)\n**2.** Choice your Gender! (Can get NonBinary | Can get change later)\n**3.** Choice your email and password! Put a fake email with @dmail.com (e.g TheGenocide@dmail.com | Can get change later)",
			color=discord.Color.orange()
		))
		await asyncio.sleep(3)
		try:
			#Channel Name 
			await ctx.send(embed=discord.Embed(
				title="Choose your channel name!",
				color=discord.Color.orange()
			).set_footer(
				text="Type your channel name!\nType abort to decline this command"
			))
			msg=await self.bot.wait_for("message", check=lambda x: x.author == ctx.author and x.channel == ctx.channel)

			if msg.content.lower() == 'abort':
				await ctx.send(embed=discord.Embed(
					title="Aborting..."
				))
				return

			else:
				#Select Gender
				embed = await ctx.send(embed=discord.Embed(
					title="Select your Gender",
					description="Select your gender with the dropdown below this embed!\nWe have Male, Female, and NonBinary",
					color=discord.Color.orange()
				), components=[
					SelectMenu(
					custom_id="Gender",
					placeholder="Choose your gender!",
					max_values=1,
					options=[
						SelectOption("Male", "value 1"),
						SelectOption("Female", "value 2"),
						SelectOption("NonBinary", "value 3")
					]
				)
				
			]
		)		
				inter = await embed.wait_for_dropdown(check=lambda inter: inter.author == ctx.author)
				label = ''.join([option.label for option in inter.select_menu.selected_options])
				await ctx.send(f"You choice **{label}**")
				await asyncio.sleep(2)

				#Select Email
				await ctx.send(embed=discord.Embed(
					title='Choose your email',
					description="Email are useful for recovering your account please make your email address\n\n**Note you dont have to put @dmail because its automatically added by the bot, Just type the email name (e.g TheGenocide, EpicUser)**",
					color=discord.Color.orange()
				))
				dmail=await self.bot.wait_for("message", check=lambda x: x.author == ctx.author and x.channel == ctx.channel)
				data = dmail.content.split("@")
				email = ''
				if 'dmail.com' in data:
					email=f"{data[0]}@dmail.com"
				else:
					email=f"{dmail.content}@dmail.com"
				await ctx.send(f"Your email is {email}")
				await asyncio.sleep(2)

				#Select Password
				await ctx.send(f"{ctx.author.mention} Check your DM!", delete_after=3)
				await ctx.author.send(embed=discord.Embed(
					title="Select your password for this account",
					description="DM me your password!",
					color=discord.Color.orange()
				))
				password=await self.bot.wait_for("message", check=lambda x: x.author == ctx.author and isinstance(x.channel, discord.DMChannel))
				await ctx.author.send(f"Your password is ||{password.content}||")
				await ctx.send(ctx.author.mention, embed=discord.Embed(
					title="Congratulation!",
					description=f"{ctx.author.mention}, your account was made! Please use the help command to see the help menu!",
					color=discord.Color.orange()
				))
				await cur.execute("INSERT INTO channel VALUES (?, ?, ?, ?, ?, ?, ?, ?)", (ctx.author.id, msg.content, 0, 0, 0, 0, 'no', 0))
				await cur2.execute("INSERT INTO info VALUES (?, ?, ?, ?, ?)", (ctx.author.id, label, 'yes', email, password.content))
				await db.commit()
				await db2.commit()
			
		
		except (discord.ext.commands.errors.CommandInvokeError, asyncio.TimeoutError) as e:
			if e == commands.errors.CommandInvokeError:
				await ctx.send(
					embed=self.channel_error
				)

			elif e == asyncio.TimeoutError:
				await ctx.send(embed=discord.Embed(
					title="Timeout!",
					color=discord.Color.red()
				).set_footer(
					text="You are too slow, Use the command again!"
				))

			else:
				raise e


	@commands.command("channel", aliases=['cha', 'chan'])
	async def _channel(self, ctx):
		obj=await helper.find_in_channel(ctx.author.id)
		if obj:
			await ctx.send(embed=discord.Embed(
				title=obj[1],
				description="You dont set a description",
				color=discord.Color.from_rgb(255, 0, 0)
			).set_thumbnail(
				url=ctx.author.avatar_url
			).add_field(
				name="Subscriber",
				value=obj[2]
			).add_field(
				name="Likes",
				value=obj[3]
			).add_field(
				name="views",
				value=obj[4]
			).add_field(
				name="Videos",
				value=obj[5]
				)
			)
		else:
			await ctx.send(embed=self.channel_error)

	@commands.command('post')
	async def _post(self, ctx, title, *,description: str = " "):
		if ctx.message.attachments:
			cur=await helper.find_in_channel(ctx.author.id)
			if cur != None:
				for x in ctx.message.attachments:
					if len(ctx.message.attachments) > 1:
						await ctx.send(embed=discord.Embed(
							color=discord.Color.red()
						).set_footer(
							text="Please send 1 video!"
						))
						return

					if x.is_spoiler():
						await ctx.send(embed=discord.Embed(
							color=discord.Color.red()
						).set_footer(
							text="Please dont send the video in spoiler!"
						))
						return
					
					if x.content_type in ['video/mp4', 'video/mp3', 'image/gif']:
						em=await ctx.send(embed=discord.Embed(
							title="Posting...",
							color=discord.Color.orange()
						).set_footer(
							text="Might take a few seconds!"
						))

						con=await helper.connect("db/video.db")
						cur=await helper.cursor(con)
						await cur.execute("INSERT INTO video VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)", (ctx.author.id, title, description, str(x), 0, 0, '', '', x.content_type))
						await con.commit()

						con=await helper.connect("db/channel.db")
						cur=await helper.cursor(con)
						await cur.execute("SELECT videos FROM channel WHERE member_id=?", (ctx.author.id,))
						data=await cur.fetchone()
						data=int(data[0])
						data += 1
						await cur.execute("UPDATE channel SET videos = ? WHERE member_id=?", (data, ctx.author.id))
						await con.commit()

						await asyncio.sleep(0.5)
						await em.edit(embed=discord.Embed(
							title="Done!",
							description=f"Posted your video!\n\nTitle: {title}\nDescription: {description}\nType: {x.content_type}",
							color=discord.Color.orange()
						).set_footer(
							text="use p!channel in order to see your stats"
						))

					else:
						await ctx.send(
							embed=discord.Embed(
								color=discord.Color.red()
						).set_footer(
							text="It need to be a video or gif :neutral_face:"
						))
			else:
				await ctx.send(embed=self.channel_error)
		else:
			await ctx.send(
				embed=discord.Embed(
					color=discord.Color.red()
				).set_footer(
					text="Put an attachment pls"
				)
			)


	@commands.command("videos")
	async def _videos(self, ctx):
		data=await helper.find_in_video(ctx.author.id, mode='all')
		video=await helper.find_in_channel(ctx.author.id)
		if not video:
			await ctx.send(embed=self.channel_error)
			return

		if not data:
			await ctx.send(embed=self.video_error)
			return

		video=int(video[5]) 
		em=discord.Embed(
			title="Video List",
			color=discord.Color.from_rgb(213, 240, 213)
		)
		em.description = ''
		
		i = 1
		for x in range(3):
			em.description += f"`{i})` {data[x][3]}\n"
			if x == video:
				break
			else:
				i += 1
		
		await ctx.send(embed=em)
			
			
	@commands.command("search")
	async def _search(self, ctx, name: str):
		if not len(name) >= 3:
			await ctx.send(embed=discord.Embed(
				color=discord.Color.red()
			).set_footer(
				text="The character must have 3 or more character"
			))
			return
		#Connection $ Cursor
		con=await helper.connect("db/video.db")
		cur=await helper.cursor(con)

		#Videos Data
		data=[x for x in await helper.find_videos(name)]
		
		#Likes & Disslikes
		likes=[x for x in await helper.find_likes(name)]
		diss=[x for x in await helper.find_disslikes(name)]
		
		#Person Already Likes & Disslikes
		old_likes=await helper.find_old_likes(name)
		old_diss=await helper.find_old_disslikes(name)

		

		i = 0
		if len(data) > 1:
			while True:
				try:
					self.review=ActionRow(
						Button(
							style=ButtonStyle.green,
							label=likes[i],
							emoji="\U0001f44d",
							custom_id="like-button",
							disable=True if ctx.author.id in old_likes else False
							
						),
						Button(
							style=ButtonStyle.red,
							label=diss[i],
							emoji="\U0001f44e",
							custom_id="disslike-button",
							disable=True if ctx.author.id in old_diss else False
							
						)
					)
					await ctx.send(i)
					msg=await ctx.send(embed=discord.Embed(
						title=f"Searched for '{name}'",
						color=discord.Color.orange()
					).set_footer(
						text=f"Search {len(data)} result"
					), components=[self.video_buttons]
				)
					file=await ctx.send(
						data[i],
						components=[self.review]
					)
					inter = await ctx.wait_for_button_click(lambda inter: inter.message.id in [msg.id, file.id] and inter.channel == ctx.channel and inter.author == ctx.author)

					if inter.clicked_button.custom_id == "right-button":  #Right Button
						if i == (len(data) - 1):
							i = 0
							await msg.delete()
							await file.delete()
							await asyncio.sleep(0.5)

						else:
							i += 1
							await msg.delete()
							await file.delete()
							await asyncio.sleep(0.5)

					elif inter.clicked_button.custom_id == "left-button": #Left Button
						if i == 0:
							i = (len(data) - 1)
							await msg.delete()
							await file.delete()
							await asyncio.sleep(0.5)
						
						else:
							i -= 1
							await msg.delete()
							await file.delete()
							await asyncio.sleep(0.5)

					elif inter.clicked_button.custom_id == "delete-button": #Delete Button
						await msg.delete()
						await file.delete()
						await ctx.send(embed=discord.Embed(
								title="Deleted All",
								description=f"{ctx.author.mention} thanks for using Tango bot :blush:",
								color=discord.Color.orange(),

							)
						)
						break

					elif inter.clicked_button.custom_id == "like-button":
						if str(ctx.author.id) in old_likes:
							await ctx.send(f"{ctx.author.mention} you already like the video")
							break
						
						elif str(ctx.author.id) in old_diss:
							await cur.execute("UPDATE videos SET member_disslikes = ? WHERE member_id=?", (old_likes + f' {str(ctx.author.id)}', str(ctx.author.id)))

						likes[i] += 1 
						await ctx.send(f"{ctx.author.mention} has Like the video!\nNow it has {likes[i]} Likes!")

						await cur.execute("UPDATE videos SET likes = ? WHERE member_id=?", (likes[i], str(ctx.author.id)))
						
						await cur.execute("UPDATE videos SET member_likes = ? WHERE member_id=?", (old_likes + f' {str(ctx.author.id)}', str(ctx.author.id)))

						await con.commit()
					
				except Exception as e:
					raise e

		elif len(data) == 1:
			msg=await ctx.send(embed=discord.Embed(
				title=f"Searched for '{name}''",
				color=discord.Color.orange()
			).set_footer(
				text=f"Found 1 result!"
			)
		)
			await ctx.send(data[i])

		else:
			msg=await ctx.send(embed=discord.Embed(
				title=f"Searched for '{name}'",
				color=discord.Color.orange()
			).set_footer(
				text=f"Found 0 result! Try again with diffreant quary"
			)
		)
	
	
def setup(bot):
	bot.add_cog(Social(bot))