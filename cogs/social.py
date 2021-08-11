import discord
import asyncio
import helper
import time
import datetime

#===============================

from discord.ext import commands
from dislash import ActionRow, Button, ButtonStyle, SelectMenu, SelectOption

class Social(commands.Cog):
	"""Social is a group of commands that contain most of the commands that other can use ;)"""
	def __init__(self, bot):
		self.bot = bot
		self.special_chars = ["!", "”", "#", "$", "%", "&", "’", ")", "(", "*", "+", ",", "-", ".", "/", ":", ";", "<", "=", ">", "?", "@", "[", "\\", "^", ">", "{", "}", "~", "`"]
		self.channel_error = discord.Embed(
			description="You haven't made your channel, Use p!start command! (Start command is under renovation)",
			color=discord.Color.red()
		)

		self.video_error = discord.Embed(
			color=discord.Color.red()
		).set_footer(
			text="You havent made a video, use p!post command!"
		)
		
		self.video_buttons=ActionRow(
			Button(
				style=ButtonStyle.blurple,
				label="",
				emoji="\U00002b05",
				custom_id="left-button"
				
			),
			Button(
				style=ButtonStyle.red,
				label="",
				emoji="\U000026d4",
				custom_id="delete-button"
				
			),
			Button(
				style=ButtonStyle.blurple,
				label="",
				emoji="\U000027a1",
				custom_id="right-button"
			)
		)

		self.button_info = ActionRow(
			Button(
				style=ButtonStyle.blurple,
				label="",
				emoji="\U00002b05",
				custom_id="left-button" #Left Button
				
			),
			Button(
				style=ButtonStyle.red,
				label="",
				emoji="<:tick_no:874284510575996968>",
				custom_id="delete-button" #Deleted Button
				
			),
			Button(
				style=ButtonStyle.blurple,
				label="",
				emoji="\U0001f522",
				custom_id="select-button" #Select Button
				
			),
			Button(
				style=ButtonStyle.blurple,
				label="",
				emoji="\U000027a1",
				custom_id="right-button" #Right Button
			)
		)


	@commands.command("profile", description="Select menu for age :p")
	async def _profile(self, ctx):
		data=await helper.find_in_channel(ctx.author.id)
		banner=data[3]
		await ctx.send(
			embed=discord.Embed(
				title="User Profile",
				description=f"Hey {ctx.author.mention}, hello there im Tango🤖 Im just checking dont mind me. Anyway have a great day and dont forget to vote me and invite me to your server, I really appreciated it! Also do you know you can get Tris after you reached 100 views. What?! You dont whats a tris? tris is Tango bot currency for buying some special features ^_^ Use p!help Market for more information",
				color=discord.Color.from_rgb(213, 240, 213)
			).add_field(
				name="Channel Name",
				value=ctx.author.name
			).add_field(
				name="Creation Date",
				value=ctx.author.created_at
			)
		)		
			








	@commands.command("start", description="Make your Tango bot account")
	@commands.is_owner()
	async def _start(self, ctx):
		db=await helper.connect("db/channel.db")
		db2=await helper.connect("db/info.db")
		cur=await helper.cursor(db)	
		cur2=await helper.cursor(db2) 
		await cur.execute("SELECT member_id FROM channel WHERE member_id=?", (int(ctx.author.id),))
		row_of_buttons = ActionRow(
			Button(
				style=ButtonStyle.green,
				emoji="\U00002705",
				custom_id="green"
			),
			Button(
				style=ButtonStyle.red,
				emoji="\U000026d4",
				custom_id="red"
			)
		)
		if await cur.fetchone() != None:
			await ctx.send(embed=discord.Embed(
				description="You already made an account",
				color=discord.Color.red()
			))
			return

		embed_message=await ctx.send(embed=discord.Embed(
			title="Time to get start!!",
			description="Hello There 👋\nTo create your channel you need to follow this 3 steps\n\n**1.** Choose your Channel name! (Can get change later)\n**2.** Choose your Gender! (Can get NonBinary | Can get change later)\n**3.** Choice your Emaul and password! Put the Email name, (e.g EpicUser123, DiscordUser432 | Can get change later)",
			color=discord.Color.from_rgb(213, 240, 213)
		).set_footer(
			text="Click the green button to continues | Click red button to decline"
		), components=[
				row_of_buttons
			]
		)
		
		while True:
			inter = await embed_message.wait_for_button_click(check=lambda inter: inter.message.id == embed_message.id)
			if inter.author != ctx.author:
				await inter.reply(embed=discord.Embed(
					description="You are not the member who use this command!",
					color=discord.Color.red()
				), 
					ephemeral=True
				)
			
			else:
				break

		button_id = inter.clicked_button.custom_id
		if button_id == "green":
			await asyncio.sleep(3)
			try:
				#Channel Name 
				await inter.reply(embed=discord.Embed(
					title="Step 1",
					description="Type your channel name without special chars!",
					color=discord.Color.from_rgb(213, 240, 213)
				).set_footer(
					text="Type abort to decline this command"
				))
				msg=await self.bot.wait_for("message", check=lambda x: x.author == ctx.author and x.channel == ctx.channel)
				
				if msg.content.lower() == "abort":
					await inter.send(embed=discord.Embed(
						description="Aborting",
						color=discord.Color.red()
					))
					return

				else:
					for x in self.special_chars:
						if x in msg.content:
							await ctx.send(embed=discord.Embed(
								description="Dont put special chars in channel name!",
								color=discord.Color.red()
							))
							return 

					await cur.execute("SELECT member_id FROM channel WHERE channel=?", (msg.content,))
					channel_data=await cur.fetchone()
					if channel_data != None:
						await inter.send(embed=discord.Embed(
							description="That User is already existed, Use the command again",
							color=discord.Color.red()
						))
						return

					
					#Select Gender
					embed = await ctx.send(embed=discord.Embed(
						title="Step 2",
						description="Select your gender with the dropdown below this embed!\nWe have Male, Female, and NonBinary",
						color=discord.Color.from_rgb(213, 240, 213)
					), components=[
							SelectMenu(
								custom_id="Gender",
								placeholder="Choose your gender!",
								max_values=1,
								options=[
									SelectOption("Male", "value 1", emoji="\U00002642"),
									SelectOption("Female", "value 2", emoji="\U00002640"),
									SelectOption("NonBinary", "value 3", emoji="\U00002b1c")
								]
							)
						]
					)		
					while True:
						inter = await embed.wait_for_dropdown(check=lambda inter: inter.author == ctx.author)
						if inter.author != ctx.author:
							await inter.reply(embed=discord.Embed(
								description="You are not the member who use this command!",
								color=discord.Color.red()
							), 
								ephemeral=True
							)
							
						
						else:
							break
						
					label = "".join([option.label for option in inter.select_menu.selected_options])
					await inter.reply(f"You choose **{label}**")
					await asyncio.sleep(2)

					#Select Email
					await ctx.send(embed=discord.Embed(
						title="Step 3",
						description="Enter your email name, enter your email without any special chars! (e.g EpicUser123, DiscordUser321)",
						color=discord.Color.from_rgb(213, 240, 213)
					))
					dmail=await self.bot.wait_for("message", check=lambda x: x.author == ctx.author and x.channel == ctx.channel)
					
					for x in self.special_chars:
						if x in dmail.content:
							await ctx.send(embed=discord.Embed(
								description="Dont put special chars in email name!",
								color=discord.Color.red()
							))
							return 

					email=f"{dmail.content}@dmail.com"
					await ctx.send(f"Your email is {email}")
					await asyncio.sleep(2)

					#Select Password
					await ctx.send(f"{ctx.author.mention} Check your DM!", delete_after=3)
					await ctx.author.send(embed=discord.Embed(
						title="Step 4",
						description="DM me your password!",
						color=discord.Color.from_rgb(213, 240, 213)
					))
					password=await self.bot.wait_for("message", check=lambda x: x.author == ctx.author and isinstance(x.channel, discord.DMChannel))
					
					for x in self.special_chars:
						if x in msg.content:
							await ctx.author.send(embed=discord.Embed(
								description="Dont put special chars in password!",
								color=discord.Color.red()
							))
							return 

					await ctx.author.send(f"Your password is ||{password.content}||")
					await cur.execute("INSERT INTO channel VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", (ctx.author.id, msg.content, "You didnt set a description", str(ctx.author.avatar_url), 0, 0, 0, 0, 0, "no", 0))
					await cur2.execute("INSERT INTO info VALUES (?, ?, ?, ?, ?)", (ctx.author.id, label, "yes", email, password.content))
					await db.commit()
					await db2.commit()
					await ctx.send(ctx.author.mention, embed=discord.Embed(
						title="Congratulation!",
						description=f"{ctx.author.mention}, your account was made! Please use the help command to see the help menu!",
						color=discord.Color.from_rgb(213, 240, 213)
					))
				
			
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

		else:
			await ctx.send(embed=discord.Embed(
				description="Aborting",
				color=discord.Color.red()
			))

	@commands.command("channel", description="Look at your channel stats", aliases=["cha", "chan"])
	async def _channel(self, ctx):
		obj=await helper.find_in_channel(ctx.author.id)
		if obj:
			await ctx.send(embed=discord.Embed(
				description=obj[2],
				color=discord.Color.from_rgb(255, 0, 0)
			).set_thumbnail(
				url=obj[3]
			).set_author(
				name=obj[1],
				url=obj[3],
				icon_url=obj[3]
			).add_field(
				name="Subscriber",
				value=obj[4]
			).add_field(
				name="Likes",
				value=obj[5]
			).add_field(
				name="views",
				value=obj[7]
			).add_field(
				name="Videos",
				value=obj[8]
				)
			)
		else:
			await ctx.send(embed=self.channel_error)

	@commands.command("post",  description="Post a video!")
	async def _post(self, ctx):
		try:
			cur=await helper.find_in_channel(ctx.author.id)
			if cur != None:
				await ctx.send(embed=discord.Embed(
					title="Title?",
					color=discord.Color.from_rgb(213, 240, 213)
				).set_footer(
					text="Type your video title!"
				).set_author(
					name=ctx.author,
					icon_url=ctx.author.avatar_url
					)
				)

				title=await self.bot.wait_for("message", check=lambda x: x.author == ctx.author and x.channel == ctx.channel)
				if len(title.content) < 4 or len(title.content) > 100:
					await ctx.send(embed=discord.Embed(
						color=discord.Color.red()
					).set_footer(
						text="Title must have 4 to 100 characters"
					))
					return

				await ctx.send(embed=discord.Embed(
					title="Description?",
					color=discord.Color.from_rgb(213, 240, 213)
				).set_footer(
					text="Type your video Description! if you dont want to include a description just enter a dot(.)"
				).set_author(
					name=ctx.author,
					icon_url=ctx.author.avatar_url
					)
				)

				description=await self.bot.wait_for("message", check=lambda x: x.author == ctx.author and x.channel == ctx.channel)
				description=description.content
				if len(description) == 1 and description == '.':
					description = ""
				elif len(description) > 256:
					await ctx.send(embed=discord.Embed(
							color=discord.Color.red()
						).set_footer(
							text="Description must have 1 to 256 characters"
						))
				await ctx.send(embed=discord.Embed(
					title="Attachment?",
					color=discord.Color.from_rgb(213, 240, 213)
				).set_footer(
					text="Send your video! must be mp4/mp3/gif"
				).set_author(
					name=ctx.author,
					icon_url=ctx.author.avatar_url
					)
				)

				attach=await self.bot.wait_for("message", check=lambda x: x.author == ctx.author and x.channel == ctx.channel)
				if attach.attachments:
					for x in attach.attachments:
						if len(attach.attachments) > 1:
							await ctx.send(embed=discord.Embed(
								color=discord.Color.red()
							).set_footer(
								text="Please send 1 video only!"
							))
							return

						if x.is_spoiler():
							await ctx.send(embed=discord.Embed(
								color=discord.Color.red()
							).set_footer(
								text="Please dont send the video in a spoiler!"
							))
							return
						
						if x.content_type in ["video/mp4", "video/mp3", "image/gif"]:
							em=await ctx.send(embed=discord.Embed(
								title="Posting...",
								color=discord.Color.from_rgb(213, 240, 213)
							).set_footer(
								text="Might take a few seconds!"
							))

							con=await helper.connect("db/channel.db")
							cur=await helper.cursor(con)
							await cur.execute("SELECT channel FROM channel WHERE member_id=?", (ctx.author.id,))
							source=await cur.fetchone()

							await asyncio.sleep(0.5)
							await em.edit(content="Are you sure you want to post this video?\nClick the green button to post this video or click the red button to cancelled this process!", embed=discord.Embed(
								title=title.content,
								url=x,
								description=description if len(description) > 1 else "This video dont have a description",
								color=discord.Color.from_rgb(213, 240, 213)
							).set_footer(
								text=f"Source : @{source[0]} | {ctx.author}"
							).set_author(
								name=f"@{source[0]}",
								url=x,
								icon_url=ctx.author.avatar_url
							).set_image(
								url=x
							).add_field(
								name="Likes",
								value=0
							).add_field(
								name="Views",
								value=0
							).add_field(
								name="Dislikes",
								value=0
							),
								components=[
									ActionRow(
										Button(
											style=ButtonStyle.green,
											emoji="\U00002705",
											custom_id="green"
										),
										Button(
											style=ButtonStyle.red,
											emoji="\U000026d4",
											custom_id="red"
										)
									)
								]
							)

							if not x.content_type == "image/gif":
								await ctx.send(x)

							inter = await ctx.wait_for_button_click(lambda inter: inter.author == ctx.author)
							id_=inter.clicked_button.custom_id
							con=await helper.connect("db/video.db")
							cur=await helper.cursor(con)

							if id_ == "green":
								await cur.execute("INSERT INTO video VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", (ctx.author.id, str(title.content), str(description), str(x), 0, 0, 0, "", "", x.content_type, int(time.time())))
								await con.commit()

								con=await helper.connect("db/channel.db")
								cur=await helper.cursor(con)
								await cur.execute("SELECT videos FROM channel WHERE member_id=?", (ctx.author.id,))
								data=await cur.fetchone()
								data=int(data[0])
								data += 1
								await cur.execute("UPDATE channel SET videos = ? WHERE member_id=?", (data, ctx.author.id))
								await con.commit()
								await em.edit(content="Posted!", 
										embed=discord.Embed(
										title=title.content,
										url=x,
										description=description if len(description) > 1 else "This video dont have a description",
										color=discord.Color.from_rgb(213, 240, 213)
										).set_footer(
											text=f"Source : @{source[0]} | {ctx.author}"
										).set_author(
											name=f"@{source[0]}",
											url=x,
											icon_url=ctx.author.avatar_url
										).set_image(
											url=x
										).add_field(
											name="Likes",
											value=0
										).add_field(
											name="Views",
											value=0
										).add_field(
											name="Dislikes",
											value=0
										))

							else:
								await em.edit(content="Declined!", 
									embed=discord.Embed(
										title=title.content,
										url=x,
										description=description if len(description) > 1 else "This video dont have a description",
										color=discord.Color.from_rgb(213, 240, 213)
										).set_footer(
											text=f"Source : @{source[0]} | {ctx.author}"
										).set_author(
											name=f"@{source[0]}",
											url=x,
											icon_url=ctx.author.avatar_url
										).set_image(
											url=x
										).add_field(
											name="Likes",
											value=0
										).add_field(
											name="Views",
											value=0
										).add_field(
											name="Dislikes",
											value=0
										))

						else:
							await ctx.send(
								embed=discord.Embed(
									color=discord.Color.red()
							).set_footer(
								text="It need to be a video or gif :neutral_face:"
							))
				else:
					await ctx.send(embed=discord.Embed(\
						color=discord.Color.red()
					).set_footer(
						text="Please send an attachment next time, the attachment must be mp3/mp4/gif."
					))
			else:
				await ctx.send(embed=self.channel_error)
		
		except Exception as e:
			raise e

	@commands.command("videos",  description="Check up your videos")
	async def _videos(self, ctx):
		data=await helper.find_in_video(ctx.author.id, mode="all")
		channel_data=await helper.find_in_channel(ctx.author.id)
		if not channel_data:
			await ctx.send(embed=self.channel_error)
			return

		if not data:
			await ctx.send(embed=self.video_error)
			return

		video=int(channel_data[8]) 
		i = video - 1
		if i < 0:
			await ctx.send(embed=self.video_error)
			return

		if video > 1: 
			while True:
				raw_date=datetime.datetime.fromtimestamp(int(data[i][10]))
				date_time=raw_date.strftime("%m/%d/%Y")
				msg=await ctx.send(embed=discord.Embed(
					title=data[i][1],
					url=data[i][3],
					description=data[i][2],
					color=discord.Color.from_rgb(213, 240, 213)
				).set_footer(
					text=f"Videos {i + 1}/{video} | Date : {date_time}",
					icon_url=channel_data[3]
				).set_author(
					name=f"{ctx.author.name} (@{channel_data[1]})",
					icon_url=channel_data[3]
				), components=[
						self.button_info
					]
				)
				
				file=await ctx.send(
					data[i][3],
					components=[
						ActionRow(
							Button(
								style=ButtonStyle.blurple,
								label=data[i][4],
								emoji="\U0001f465",
								custom_id="views-button",
								disabled=True
							),
							Button(
								style=ButtonStyle.grey,
								label=date_time,
								emoji="\U0000231b",
								custom_id="date-button",
								disabled=True
							),
							Button(
								style=ButtonStyle.green,
								label=data[i][5],
								emoji="\U0001f44d",
								custom_id="like-button",
								disabled=True	
							),
							Button(
								style=ButtonStyle.red,
								label=data[i][6],
								emoji="\U0001f44e",
								custom_id="dislike-button",
								disabled=True
								
							)
						)
					]
				)
				while True:
					inter = await ctx.wait_for_button_click(lambda inter: inter.author == ctx.author and inter.message.id == msg.id and inter.channel == ctx.channel)
					if inter.author != ctx.author:
						await inter.reply(embed=discord.Embed(
							description="You are not the member who use this command!",
							color=discord.Color.red()
						),
							ephemeral=True
						)
						
					else:
						break
					
				if inter.clicked_button.custom_id == "left-button": #Left Button
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

				elif inter.clicked_button.custom_id == "right-button":  #Right Button
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


				elif inter.clicked_button.custom_id == "delete-button": #Delete Button
					await msg.delete()
					await file.delete()
					await ctx.send(embed=discord.Embed(
							description=f"{ctx.author.mention} thanks for using Tango bot :blush:",
							color=discord.Color.from_rgb(213, 240, 213),
						)
					)
					break

				elif inter.clicked_button.custom_id == "select-button": #Select Button
					try:
						await inter.reply(
							ctx.author.mention, 
							embed=discord.Embed(
								description=f"What video you want to view? You have **{video}** videos",
								color=discord.Color.from_rgb(213, 240, 213)
							))					
						while True:
							select=await self.bot.wait_for("message", check=lambda x: x.author == ctx.author and x.channel == ctx.channel, timeout=20)
							
							try:
								page=int(select.content)
							except ValueError:
								await ctx.send("The message must be a number not a letter(s)")

							if page > video:
								await ctx.send("Number is Too large, enter it again with smaller one")
								await asyncio.sleep(0.5)
							
							elif page <= 0:
								await ctx.send("Number cannot be minus or zero, enter it again with bigger one")
								await asyncio.sleep(0.5)
							
							else:
								page = page - 1
								i = page
								await msg.delete()
								await file.delete()
								await asyncio.sleep(0.5)
								break

					except Exception as e:
						raise e

		else:
			msg=await ctx.send(embed=discord.Embed(
				title=data[i][1],
				url=data[i][3],
				description=data[i][2],
				color=discord.Color.from_rgb(213, 240, 213)
			).set_footer(
				text=f"Video {i + 1}/{video} | Source : @{channel_data[1]}",
				icon_url=channel_data[3]
			).set_author(
				name=f"{ctx.author.name} (@{channel_data[1]})",
				icon_url=channel_data[3]
			)
		)
			
			await ctx.send(
					data[i][3],
					components=[
						ActionRow(
							Button(
								style=ButtonStyle.green,
								label=data[i][5],
								emoji="\U0001f44d",
								custom_id="like-button",
								disabled=True	
							),
							Button(
								style=ButtonStyle.blurple,
								label=data[i][4],
								emoji="\U0001f465",
								custom_id="views-button",
								disabled=True
							),
							Button(
								style=ButtonStyle.red,
								label=data[i][6],
								emoji="\U0001f44e",
								custom_id="dislike-button",
								disabled=True
								
							)
						)
					]
				)		


			
	@commands.command("search", description="Search up videos that got posted by other members!")
	async def _search(self, ctx, *,name):
		status=True
		if not len(name) >= 3:
			await ctx.send(embed=discord.Embed(
				color=discord.Color.red()
			).set_footer(
				text="The name argument must have 3 or more characters"
			))
			return

		videos=await helper.find_videos(name)
		con=await helper.connect("db/video.db")
		cur=await helper.cursor(con)
		data=[x for x in videos]
		

		i = 0
		if len(data) > 1:
			channel_data=await helper.find_in_channel(data[i][8])
			print(channel_data)
			while True:
				try:
					status = True					
					num = i + 1
					user=await self.bot.fetch_user(channel_data[0])
					msg=await ctx.send(
						embed=discord.Embed(
							title=data[i][1],
							url=data[i][0],
							description=data[i][2],
							color=discord.Color.from_rgb(213, 240, 213)
						).set_footer(
							text=f"Videos {num}/{len(data)} | Source : @{channel_data[1]}",
							icon_url=channel_data[3]
						).set_author(
							name=f"{user.name} (@{channel_data[1]})",
							icon_url=channel_data[3]
						),
						
						components=[self.video_buttons]
					)
					file=await ctx.send(
						data[i][0],
						components=[
							ActionRow(
								Button(
									style=ButtonStyle.green,
									label=data[i][4],
									emoji="\U0001f44d",
									custom_id="like-button",
									disabled=True if str(ctx.author.id) in data[i][6] else False
								),
								Button(
									style=ButtonStyle.blurple,
									label=data[i][3],
									emoji="\U0001f465",
									custom_id="view-button",
									disabled=True
								),
								Button(
									style=ButtonStyle.red,
									label=data[i][5],
									emoji="\U0001f44e",
									custom_id="dislike-button",
									disabled=True if str(ctx.author.id) in data[i][7] else False
								)
							)
						]
					)
					await cur.execute("UPDATE video SET views = ? WHERE link = ?", (data[i][3] + 1 if int(data[i][8]) != ctx.author.id else data[i][3] + 0, data[i][0]))
					await con.commit()
					inter = await ctx.wait_for_button_click(lambda inter: inter.message.id == msg.id or inter.message.id == file.id and inter.channel == ctx.channel)	
					author=await helper.find_in_channel(inter.author.id)
					
					if author == None:
						await ctx.send(embed=self.channel_error)
						return

					button_id = inter.clicked_button.custom_id
					if button_id == "right-button":  #Right Button
						if inter.author == ctx.author:
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
						else:
							await inter.reply(embed=discord.Embed(
								description=f"You can only give a like and a dislikes! Ask {ctx.author.mention} to click this button!",
								color=discord.Color.red()
							),
								ephemeral=True
							)

					elif button_id == "left-button": #Left Button
						if inter.author == ctx.author:
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
						else:
							await inter.reply(embed=discord.Embed(
								description=f"You can only give a like and a dislikes! Ask {ctx.author.mention} to click this button!",
								color=discord.Color.red()
							),
								ephemeral=True
							)

					elif button_id == "delete-button": #Delete Button
						if inter.author == ctx.author:
							await msg.delete()
							await file.delete()
							await ctx.send(embed=discord.Embed(
									description=f"{ctx.author.mention} thanks for using Tango bot :blush:",
									color=discord.Color.from_rgb(213, 240, 213),
								)
							)
							break

						else:
							await inter.reply(embed=discord.Embed(
								description=f"You can only give a like and a dislikes! Ask {ctx.author.mention} to click this button!",
								color=discord.Color.red()
							),
								ephemeral=True
							)

					elif button_id == "like-button": #Like Button
						old_likes = f"{data[i][6]} {str(ctx.author.id)}"
						old_dislikes = data[i][7].replace(str(ctx.author.id), "")
						if str(ctx.author.id) in data[i][7]:
							await cur.execute("UPDATE video SET old_dislikes = ? WHERE link = ?", (old_dislikes, str(data[i][0])))
							await cur.execute("UPDATE video SET dislikes = ? WHERE link = ?", (data[i][5] - 1, str(data[i][0])))

						await cur.execute("UPDATE video SET old_likes = ? WHERE link = ?", (old_likes, str(data[i][0])))
						await cur.execute("UPDATE video SET likes = ? WHERE link = ?", (int(data[i][4]) + 1, str(data[i][0])))
						await inter.send(embed=discord.Embed(
							description=f"{ctx.author.mention} Liked this video!",
							color=discord.Color.from_rgb(213, 240, 213)
						),
							ephemeral=True
						)
						await con.commit()
						while True:
							inter = await ctx.wait_for_button_click(lambda inter: inter.message.id == msg.id or inter.message.id == file.id and inter.channel == ctx.channel)	
							button_id = inter.clicked_button.custom_id
							if button_id == "right-button":  #Right Button
								if inter.author == ctx.author:
									if i == (len(data) - 1):
										i = 0
										await msg.delete()
										await file.delete()
										await asyncio.sleep(0.5)
										break

									else:
										i += 1
										await msg.delete()
										await file.delete()
										await asyncio.sleep(0.5)
										break
								else:
									await inter.reply(embed=discord.Embed(
										description=f"You can only give a like and a dislikes! Ask {ctx.author.mention} to click this button!",
										color=discord.Color.red()
									),
										ephemeral=True
									)

							elif button_id == "left-button": #Left Button
								if inter.author == ctx.author:
									if i == 0:
										i = (len(data) - 1)
										await msg.delete()
										await file.delete()
										await asyncio.sleep(0.5)
										break
									
									else:
										i -= 1
										await msg.delete()
										await file.delete()
										await asyncio.sleep(0.5)
										break
								else:
									await inter.reply(embed=discord.Embed(
										description=f"You can only give a like and a dislikes! Ask {ctx.author.mention} to click this button!",
										color=discord.Color.red()
									),
										ephemeral=True
									)

							elif button_id == "delete-button": #Delete Button
								if inter.author == ctx.author:
									await msg.delete()
									await file.delete()
									await ctx.send(embed=discord.Embed(
											description=f"{ctx.author.mention} thanks for using Tango bot :blush:",
											color=discord.Color.from_rgb(213, 240, 213),
										)
									)
									status = False
									break

								else:
									await inter.reply(embed=discord.Embed(
										description=f"You can only give a like and a dislikes! Ask {ctx.author.mention} to click this button!",
										color=discord.Color.red()
									),
										ephemeral=True
									)
								
							if status == False:
								break
	
					elif button_id == "dislike-button": #Dislike Button
						old_likes = f"{data[i][7]} {str(ctx.author.id)}"
						old_dislikes = data[i][6].replace(str(ctx.author.id), "")
						if str(ctx.author.id) in data[i][6]:
							await cur.execute("UPDATE video SET old_likes = ? WHERE link = ?", (old_dislikes, str(data[i][0])))
							await cur.execute("UPDATE video SET likes = ? WHERE link = ?", (data[i][4] - 1, str(data[i][0])))
						
						await cur.execute("UPDATE video SET old_dislikes = ? WHERE link = ?", (old_likes, str(data[i][0])))
						await cur.execute("UPDATE video SET dislikes = ? WHERE link = ?", (int(data[i][5]) + 1, str(data[i][0])))
						await inter.send(embed=discord.Embed(
							description=f"{ctx.author.mention} Disliked this video!",
							color=discord.Color.from_rgb(213, 240, 213)
						),
							ephemeral=True
						)
						await con.commit()
						while True:
							inter = await ctx.wait_for_button_click(lambda inter: inter.message.id == msg.id or inter.message.id == file.id and inter.channel == ctx.channel)	
							button_id = inter.clicked_button.custom_id
							if button_id == "right-button":  #Right Button
								if inter.author == ctx.author:
									if i == (len(data) - 1):
										i = 0
										await msg.delete()
										await file.delete()
										await asyncio.sleep(0.5)
										break

									else:
										i += 1
										await msg.delete()
										await file.delete()
										await asyncio.sleep(0.5)
										break
								else:
									await inter.reply(embed=discord.Embed(
										description=f"You can only give a like and a dislikes! Ask {ctx.author.mention} to click this button!",
										color=discord.Color.red()
									),
										ephemeral=True
									)

							elif button_id == "left-button": #Left Button
								if inter.author == ctx.author:
									if i == 0:
										i = (len(data) - 1)
										await msg.delete()
										await file.delete()
										await asyncio.sleep(0.5)
										break
									
									else:
										i -= 1
										await msg.delete()
										await file.delete()
										await asyncio.sleep(0.5)
										break
								else:
									await inter.reply(embed=discord.Embed(
										description=f"You can only give a like and a dislikes! Ask {ctx.author.mention} to click this button!",
										color=discord.Color.red()
									),
										ephemeral=True
									)

							elif button_id == "delete-button": #Delete Button
								if inter.author == ctx.author:
									await msg.delete()
									await file.delete()
									await ctx.send(embed=discord.Embed(
											description=f"{ctx.author.mention} thanks for using Tango bot :blush:",
											color=discord.Color.from_rgb(213, 240, 213),
										)
									)
									status = False
									break

								else:
									await inter.reply(embed=discord.Embed(
										description=f"You can only give a like and a dislikes! Ask {ctx.author.mention} to click this button!",
										color=discord.Color.red()
									),
										ephemeral=True
									)
							
							if status == False:
								break
						
				except Exception as e:
					raise e

		elif len(data) == 1:
			channel_data=await helper.find_in_channel(data[i][0])
			msg=await ctx.send(
				embed=discord.Embed(
					title=data[i][1],
					url=data[i][0],
					description=data[i][2],
					color=discord.Color.from_rgb(213, 240, 213)
				).set_footer(
					text=f"Videos 1/1 | Source : @{channel_data[1]}"
				).set_author(
					name=f"{ctx.author.name} (@{channel_data[1]})",
					icon_url=channel_data[3]
				),

				components=[
					ActionRow(
						Button(
							style=ButtonStyle.blurple,
							label="",
							emoji="\U00002b05",
							custom_id="left-button",
							disabled=True
						),
						Button(
							style=ButtonStyle.red,
							label="",
							emoji="\U000026d4",
							custom_id="delete-button",
							disabled=False
						),
						Button(
							style=ButtonStyle.blurple,
							label="",
							emoji="\U000027a1",
							custom_id="right-button",
							disabled=True
						)
					)
				]
			) 
			file=await ctx.send(
				data[i][0],
				components=[
					ActionRow(
						Button(
							style=ButtonStyle.green,
							label=data[i][4],
							emoji="\U0001f44d",
							custom_id="like-button",
							disabled=True if str(ctx.author.id) in data[i][6] else False
						),
						Button(
							style=ButtonStyle.blurple,
							label=data[i][3],
							emoji="\U0001f465",
							custom_id="view-button",
							disabled=True
						),
						Button(
							style=ButtonStyle.red,
							label=data[i][5],
							emoji="\U0001f44e",
							custom_id="dislike-button",
							disabled=True if str(ctx.author.id) in data[i][7] else False
						)
					)
				]
			)
			while True:
				try:
					await cur.execute("UPDATE video SET views = ? WHERE link = ?", (data[i][3] + 1 if int(data[i][8]) != ctx.author.id else data[i][3] + 0, data[i][0]))
					await con.commit()
					while True:
						inter = await ctx.wait_for_button_click(lambda inter: inter.message.id == msg.id or inter.message.id == file.id and inter.channel == ctx.channel and inter.author == ctx.author)
						if inter.author != ctx.author:
							await inter.reply(embed=discord.Embed(
								description="You are not the member who use this command!",
								color=discord.Color.red()
							), 
								ephemeral=True
							)
							
						else:
							break
					button_id = inter.clicked_button.custom_id
					if button_id == "right-button":  #Right Button
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

					elif button_id == "left-button": #Left Button
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

					elif button_id == "delete-button": #Delete Button
						await msg.delete()
						await file.delete()
						await ctx.send(embed=discord.Embed(
								description=f"{ctx.author.mention} thanks for using Tango bot :blush:",
								color=discord.Color.from_rgb(213, 240, 213),

							)
						)
						break

					elif button_id == "like-button": #like-button
						old_likes = f"{data[i][6]} {str(ctx.author.id)}"
						old_dislikes = data[i][7].replace(str(ctx.author.id), "")
						if str(ctx.author.id) in data[i][7]:
							await cur.execute("UPDATE video SET old_dislikes = ? WHERE link = ?", (old_dislikes, str(data[i][0])))
							await cur.execute("UPDATE video SET dislikes = ? WHERE link = ?", (data[i][5] - 1, str(data[i][0])))

						await cur.execute("UPDATE video SET old_likes = ? WHERE link = ?", (old_likes, str(data[i][0])))
						await cur.execute("UPDATE video SET likes = ? WHERE link = ?", (int(data[i][4]) + 1, str(data[i][0])))
						await inter.send(embed=discord.Embed(
							description=f"{ctx.author.mention} Liked this video!",
							color=discord.Color.from_rgb(213, 240, 213)
						),
							ephemeral=True
						)
						await con.commit()
						 
					elif button_id == "dislike-button": #dislike-button
						old_likes = f"{data[i][7]} {str(ctx.author.id)}"
						old_dislikes = data[i][6].replace(str(ctx.author.id), "")
						if str(ctx.author.id) in data[i][6]:
							await cur.execute("UPDATE video SET old_likes = ? WHERE link = ?", (old_dislikes, str(data[i][0])))
							await cur.execute("UPDATE video SET likes = ? WHERE link = ?", (data[i][4] - 1, str(data[i][0])))
						
						await cur.execute("UPDATE video SET old_dislikes = ? WHERE link = ?", (old_likes, str(data[i][0])))
						await cur.execute("UPDATE video SET dislikes = ? WHERE link = ?", (int(data[i][5]) + 1, str(data[i][0])))
						await inter.send(embed=discord.Embed(
							description=f"{ctx.author.mention} Disliked this video!",
							color=discord.Color.from_rgb(213, 240, 213)
						),
							ephemeral=True
						)
						await con.commit()

				except Exception as e:
					raise e
		else:
			msg=await ctx.send(embed=discord.Embed(
				title=f"Searched for '{name}'",
				color=discord.Color.from_rgb(213, 240, 213)
			).set_footer(
				text=f"Found 0 result! Try again with diffreant quary"
			)
		)
	
	@commands.command("setting", description="Setting up your channel and profile info", aliases=['set'])
	async def _setting(self, ctx):
		db=await helper.connect("db/channel.db")
		db2=await helper.connect("db/info.db")
		cur=await helper.cursor(db)
		info=await helper.cursor(db2)
		user=await helper.find_user(ctx.author.id)
		if user == False:
			await ctx.send(embed=self.channel_error)
			return

		embed=await ctx.send(embed=discord.Embed(
			title="Setting Menu",
			description="Is there anything i could help?",
			color=discord.Color.from_rgb(213, 240, 213)
		), 
		components=[
				SelectMenu(
					custom_id="Option",
					placeholder="Choose your change",
					max_values=1,
					options=[
						SelectOption("Channel Name", "channel", emoji="\U0001f4db"),
						SelectOption("Channel Description", "description", emoji="\U0001f6d1"),
						SelectOption("Channel Banner", "banner", emoji="\U0001f5bc"),

						SelectOption("User Gender", "gender", emoji="\U00002642"),
						SelectOption("User Email", "email", emoji="\U0001f4e7"),
						SelectOption("User Password", "password", emoji="\U0001f6c2")

					]
				)
				
			]
		)
		try:
			while True:
				inter = await embed.wait_for_dropdown(check=lambda inter: inter.author == ctx.author)
				if inter.author != ctx.author:
					await inter.reply(embed=discord.Embed(
						description="You are not the member who use this command!",
						color=discord.Color.red()
					), 
						ephemeral=True
					)
					
				else:
					break
			label = "".join([option.label for option in inter.select_menu.selected_options])
			value= "".join([option.value for option in inter.select_menu.selected_options])
			if value == "channel":
				await inter.reply(embed=discord.Embed(
					title="Type your change",
					description=f"Type your new {label}",
					color=discord.Color.from_rgb(213, 240, 213)
				).set_footer(
					text="You have 120 seconds to do this"
				))
				msg=await self.bot.wait_for("message", check=lambda x: x.author == ctx.author and x.channel == ctx.channel, timeout=120)
				await cur.execute("UPDATE channel SET channel = ? WHERE member_id = ?", (msg.content, ctx.author.id))
				await ctx.send(embed=discord.Embed(
						description="Done! Check it using p!channel",
						color=discord.Color.from_rgb(213, 240, 213)
					)
				)
				await db.commit()
				await cur.close()

			elif value == "description":
				await inter.reply(embed=discord.Embed(
					title="Type your change",
					description=f"Type your new {label}",
					color=discord.Color.from_rgb(213, 240, 213)
				).set_footer(
					text="You have 120 seconds to do this"
				))
				msg=await self.bot.wait_for("message", check=lambda x: x.author == ctx.author and x.channel == ctx.channel, timeout=120)
				await cur.execute("UPDATE channel SET description = ? WHERE member_id = ?", (msg.content, ctx.author.id))
				await ctx.send(embed=discord.Embed(
						description="Done! Check it using p!channel",
						color=discord.Color.from_rgb(213, 240, 213)
					)
				)
				
				await db.commit()
				await cur.close()

			elif value == "banner":
				await inter.reply(embed=discord.Embed(
					title="Type your change",
					description=f"Type your new {label}\nSend me an image",
					color=discord.Color.from_rgb(213, 240, 213)
				).set_footer(
					text="You have 120 seconds to do this"
				))
				msg=await self.bot.wait_for("message", check=lambda x: x.author == ctx.author and x.channel == ctx.channel, timeout=120)
				
				if msg.attachments or msg.content.startswith("http"):
					if msg.attachments:
						for x in msg.attachments:
							await cur.execute("UPDATE channel SET banner = ? WHERE member_id = ?", (str(x), ctx.author.id))
							await ctx.send(embed=discord.Embed(
									description="Done! Check it using p!channel",
									color=discord.Color.from_rgb(213, 240, 213)
								)
							)
							break
						
					else:
						await cur.execute("UPDATE channel SET banner = ? WHERE member_id = ?", (msg.content, ctx.author.id))
						await ctx.send(embed=discord.Embed(
								description="Done! Check it using p!channel",
								color=discord.Color.from_rgb(213, 240, 213)
							)
						)
						
				await db.commit()
				await cur.close()
				
				
			
	#=================================================

			elif value == "gender":
				Message=await inter.reply(embed=discord.Embed(
					title="Select your change",
					description="Select your gender",
					color=discord.Color.from_rgb(213, 240, 213)
				).set_footer(
					text="You have 120 seconds to do this"
				), components=[
						SelectMenu(
						custom_id="Gender",
						placeholder="Choose your gender!",
						max_values=1,
						options=[
							SelectOption("Male", "value 1", emoji="\U00002642"),
							SelectOption("Female", "value 2", emoji="\U00002640"),
							SelectOption("NonBinary", "value 3", emoji="\U00002b1c")
						]
					)
				]
			)
				gender = await Message.wait_for_dropdown(check=lambda inter: inter.author == ctx.author and inter.message == Message)
				label = "".join([option.label for option in gender.select_menu.selected_options])
				await gender.reply(embed=discord.Embed(
						description="Done! Check it using p!info",
						color=discord.Color.from_rgb(213, 240, 213)
					)
				)
			
				await info.execute("UPDATE info SET gender = ? WHERE member_id = ?", (label, ctx.author.id))
				
				await db2.commit()
				await info.close()

			elif value == "email":
				await inter.reply(embed=discord.Embed(
					title="Type your change",
					description=f"Type your new Email without special chars! (e.g EpicUser123, EpicDiscord123)",
					color=discord.Color.from_rgb(213, 240, 213)
				).set_footer(
					text="You have 120 seconds to do this"
				))
				msg=await self.bot.wait_for("message", check=lambda x: x.author == ctx.author and x.channel == ctx.channel, timeout=120)

				for x in self.special_chars:
					if x in msg.content:
						await ctx.send(embed=discord.Embed(
							description="Dont put special chars in email!",
							color=discord.Color.red()
						))
						return 

	
				await info.execute("UPDATE info SET email = ? WHERE member_id = ?", (msg.content, ctx.author.id))
				await ctx.send(embed=discord.Embed(
						description="Done! Check it using p!channel",
						color=discord.Color.from_rgb(213, 240, 213)
					)
				)

				await db2.commit()
				await info.close()

			elif value == "password":
				await inter.reply(f"{ctx.author.mention} check your DM")
				await ctx.author.send(embed=discord.Embed(
					title="Type your change",
					description=f"Type your new Password",
					color=discord.Color.from_rgb(213, 240, 213)
				).set_footer(
					text="You have 120 seconds to do this"
				))
				msg=await self.bot.wait_for("message", check=lambda x: x.author == ctx.author and isinstance(x.channel, discord.DMChannel), timeout=120)
				
				for x in self.special_chars:
					if x in msg.content:
						await ctx.author.send(embed=discord.Embed(
							description="Dont put special chars in password!",
							color=discord.Color.red()
						))
						return 

				await ctx.author.send(f"Your password are ||{msg.content}||")
				await info.execute("UPDATE info SET password = ? WHERE member_id = ?", (msg.content, ctx.author.id))
				await ctx.send(ctx.author.mention, embed=discord.Embed(
						description="Done! Check it using p!info",
						color=discord.Color.from_rgb(213, 240, 213)
					)
				)

				await db2.commit()
				await info.close()

		except asyncio.TimeoutError:
			await ctx.send(embed=discord.Embed(
				description="Too late, type the command again"
			))
			return

def setup(bot):
	bot.add_cog(Social(bot))