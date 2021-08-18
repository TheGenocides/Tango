import discord
import asyncio
import helper
import time
import datetime
import ast

#===============================

from uuid import uuid4
from discord.ext import commands
from dislash import ActionRow, Button, ButtonStyle, SelectMenu, SelectOption, ResponseType

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



	@commands.command("profile", description="Select menu for age :p")
	async def _profile(self, ctx):
		data=await helper.find_in_channel(ctx.author.id)
		info=await helper.find_in_info(ctx.author.id)
		if not data or not info:
			await ctx.send(embed=self.channel_error)
			return

		await ctx.send(
			embed=discord.Embed(
				title="Profile Menu!",
				description=data[2],
				color=discord.Color.from_rgb(213, 240, 213),
				timestamp=ctx.message.created_at
					).set_author(
						name=f"{ctx.author.name} (@{data[1]})",
						icon_url=data[3]
					).set_footer(
						text=f"Source: @{data[1]} | ID: {ctx.author.id}",
						icon_url=data[3]
					).add_field(
						name="<:follow:875659362264309791> Subs",
						value=data[4]
					).add_field(
						name="<:blurple_camera:875659362331394058> Videos",
						value=data[8]
					).add_field(
						name="🫂 Views",
						value=data[7]
					).add_field(
						name="<:likes:875659362343993404> Likes",
						value=data[5]
					).add_field(
						name="<:dislikes:875659362264309821> Dislikes",
						value=data[6]
					).add_field(
						name="\u200b",
						value="\u200b"
					).add_field(
						name="Account Information",
						value="Here is all of your account information! You can change it using p!set command!",
						inline=False
					).add_field(
						name="🫂 Gender",
						value=info[1]
					).add_field(
						name="📧 email",
						value=info[3]
					).add_field(
						name="🔑 Password",
						value="||[Password Redacted]||",
						inline=False
					).add_field(
						name="⌛ Account Age",
						value=info[5]
					)
				)		

	@commands.command("start", description="Make your Tango bot account")
	async def _start(self, ctx):
		# if not ctx.author.id in self.bot.owner_ids:
		# 	await ctx.send("Start command is under renovation!")
		# 	return
		
		age=time.time()
		db=await helper.connect("db/channel.db")
		db2=await helper.connect("db/info.db")
		cur=await helper.cursor(db)	
		cur2=await helper.cursor(db2) 
		channel_data=await helper.find_in_channel(ctx.author.id)

		buttons = ActionRow(
			Button(
				style=ButtonStyle.green,
				emoji="<:tick_yes:874284510135607350>",
				custom_id="green"
			),
			Button(
				style=ButtonStyle.red,
				emoji="<:tick_no:874284510575996968>",
				custom_id="red"
			)
		)

		if channel_data != None:
			await ctx.send(embed=discord.Embed(
				description="You already made an account",
				color=discord.Color.red()
			))
			return

		embed_message=await ctx.send(embed=discord.Embed(
			title="Time to get start!!",
			description="Hello There 👋\nYou have 1 to 5 steps to make your TangoBot account, you can always press abort button to cancel the command! Click the green button to continues or click red button to cancel this command. The bot will guide the rest",
			color=discord.Color.from_rgb(213, 240, 213)
		), components=[
				buttons
			]
		)
		
		on_click=embed_message.create_click_listener(timeout=120)
		

		@on_click.not_from_user(ctx.author, cancel_others=True, reset_timeout=False)
		async def _not_from_author(inter):
			await inter.reply(
				type=ResponseType.ChannelMessageWithSource,
				embed=discord.Embed(
					description="You are not the member who use this command!",
					color=discord.Color.red()
				), 
					ephemeral=True
				)

		
		@on_click.matching_id("red")
		async def _red(inter):
			await inter.reply(
				type=7,
				embed=discord.Embed(
				description="Aborting",
				color=discord.Color.red()
			))

			on_click.kill()

		@on_click.matching_id("green")
		async def _green(inter):
			nonlocal on_click
			try:
				#Channel Name 
				await inter.reply(
					type=ResponseType.ChannelMessageWithSource,
					embed=discord.Embed(
					title="Step 1",
					description="Type your channel name without special chars! Minimum of 3 to 13 characters!",
					color=discord.Color.from_rgb(213, 240, 213)
				).set_footer(
					text="Type abort to decline this command"
				))
				msg=await self.bot.wait_for("message", check=lambda x: x.author == ctx.author and x.channel == ctx.channel)
				
				if msg.content.lower() == "abort":
					await ctx.send(embed=discord.Embed(
						description="Aborting",
						color=discord.Color.red()
					))
					on_click.kill()
					return

				else:
					for x in self.special_chars:
						if x in msg.content:
							await ctx.send(embed=discord.Embed(
								description="Dont put special chars in channel name!",
								color=discord.Color.red()
							))
							on_click.kill()
							return 

					if len(msg.content) > 13 or len(msg.content) < 3:
						await ctx.send(embed=discord.Embed(
							description="You put too much or too little characters!",
							color=discord.Color.red()
						))
						on_click.kill()
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
									SelectOption("Male", "value 1", emoji="\U00002642", description="A Male Gender Option"),
									SelectOption("Female", "value 2", emoji="\U00002640", description="A Female Gender Option"),
									SelectOption("NonBinary", "value 3", emoji="\U00002b1c", description="A Nonbinary option")
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

					#Select email
					await ctx.send(embed=discord.Embed(
						title="Step 3",
						description="Enter your email name, enter your email without any special chars! (e.g EpicUser123, DiscordUser321) You need a minimum of 5 to 13 characters",
						color=discord.Color.from_rgb(213, 240, 213)
					))
					email=await self.bot.wait_for("message", check=lambda x: x.author == ctx.author and x.channel == ctx.channel)

					if email.content.lower() == "abort":
						await ctx.send(embed=discord.Embed(
						description="Aborting",
						color=discord.Color.red()
					))
						on_click.kill()
						return

					for x in self.special_chars:
						if x in email.content:
							await ctx.send(embed=discord.Embed(
								description="Dont put special chars in email name!",
								color=discord.Color.red()
							))
							on_click.kill()
							return 

					if len(email.content) > 15 or len(email.content) < 5:
						await ctx.send(embed=discord.Embed(
							description="You put too much or too little characters!",
							color=discord.Color.red()
						))
						on_click.kill()
						return

					email=f"{email.content}@email.com"
					await ctx.send(f"Your email is {email}")
					await asyncio.sleep(2)

					#Select Password
					await ctx.send(f"{ctx.author.mention} Check your DM!")
					await ctx.author.send(embed=discord.Embed(
						title="Step 4",
						description="DM me your password! You need a minimum of 5 to 15 characters",
						color=discord.Color.from_rgb(213, 240, 213)
					))
					password=await self.bot.wait_for("message", check=lambda x: x.author == ctx.author and isinstance(x.channel, discord.DMChannel))
					
					if password.content.lower() == "abort":
						await ctx.send(embed=discord.Embed(
						description="Aborting",
						color=discord.Color.red()
					))
						on_click.kill()
						return

					for x in self.special_chars:
						if x in msg.content:
							await ctx.author.send(embed=discord.Embed(
								description="Dont put special chars in password!",
								color=discord.Color.red()
							))
							on_click.kill()
							return

					if len(password.content) > 15 or len(password.content) < 5:
						await ctx.author.send(embed=discord.Embed(
							description="You put too much or too little characters!",
							color=discord.Color.red()
						))
						on_click.kill()
						return 

					await ctx.author.send(f"Your password is ||{password.content}|| Continue to {ctx.channel.mention}!")
					

					confirm=await ctx.send(
						f"**Little bit more!**\n{ctx.author.mention} You just need to confirm all of your credentials. We(TangoBot devs) respect all of your privacy, For your information we are only gonna store your Member-ID and your Tango bot account password which is bind to your ID!\nPlease click the green button to continue or the red button to decline this!",
						embed=discord.Embed(
						title="<a:moving_gear:874897860469088296> Profile",
						description="<a:moving_gear:874897860469088296> Set a new description, banner, using p!set command! also you can change channel name, email, password, and gender so dont you worry!",
						color=discord.Color.from_rgb(213, 240, 213),
						timestamp=ctx.message.created_at
					).set_author(
						name=f"{ctx.author.name} (@{msg.content})",
						icon_url=ctx.author.avatar_url
					).set_footer(
						text=f"Source: @{msg.content} | ID: {ctx.author.id}",
						icon_url=ctx.author.avatar_url
					).add_field(
						name="<:follow:875659362264309791> Subs",
						value=0
					).add_field(
						name="<:blurple_camera:875659362331394058> Videos",
						value=0
					).add_field(
						name="🫂 Views",
						value=0
					).add_field(
						name="<:likes:875659362343993404> Likes",
						value=0
					).add_field(
						name="<:dislikes:875659362264309821> Dislikes",
						value=0
					).add_field(
						name="\u200b",
						value="\u200b"
					).add_field(
						name="Account Information",
						value="<a:moving_gear:874897860469088296> Here is all of your account information! You can change it using p!set command!",
						inline=False
					).add_field(
						name="🫂 Gender",
						value=label
					).add_field(
						name="📧 email",
						value=email
					).add_field(
						name="🔑 Password",
						value="||Password Redacted||",
						inline=False
					).add_field(
						name="⌛ Account Age",
						value=f"<t:{int(age)}:F>"
					),
					components=[
						buttons
					]
				)
					on_click.kill()
					on_click=confirm.create_click_listener(timeout=120.0)
					
					@on_click.not_from_user(ctx.author, cancel_others=True)
					async def _not_From_user(inter):
						await inter.reply(
							type=ResponseType.ChannelMessageWithSource,
							embed=discord.Embed(
								description="You are not the member who use this command!",
								color=discord.Color.red()
							), 
								ephemeral=True
							)

					@on_click.matching_id("green")
					async def _Green(inter):
						await cur.execute("INSERT INTO channel VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", (ctx.author.id, msg.content, "Set a new description, banner, using p!set command! also you can change channel name, email, password, and gender so dont you worry!", str(ctx.author.avatar_url), 0, 0, 0, 0, 0, "no", 0))
						await cur2.execute("INSERT INTO info VALUES (?, ?, ?, ?, ?, ?)", (ctx.author.id, label, "yes", email, password.content, f"<t:{int(age)}:F>"))
						await db.commit()
						await db2.commit()
						await inter.reply(
							"**Done**\nYou made your account! Now use the `p!help Social` for all commands regarding Social Media!",
							type=ResponseType.UpdateMessage,
							embed=discord.Embed(
								title="<a:moving_gear:874897860469088296> Profile",
								description="<a:moving_gear:874897860469088296> Set a new description, banner, using p!set command! also you can change channel name, email, password, and gender so dont you worry!",
								color=discord.Color.from_rgb(213, 240, 213),
								timestamp=ctx.message.created_at
							).set_author(
								name=f"{ctx.author.name} (@{msg.content})",
								icon_url=ctx.author.avatar_url
							).set_footer(
								text=f"Source: @{msg.content} | ID: {ctx.author.id}",
								icon_url=ctx.author.avatar_url
							).add_field(
								name="<:follow:875659362264309791> Subs",
								value=0
							).add_field(
								name="<:blurple_camera:875659362331394058> Videos",
								value=0
							).add_field(
								name="🫂 Views",
								value=0
							).add_field(
								name="<:likes:875659362343993404> Likes",
								value=0
							).add_field(
								name="<:dislikes:875659362264309821> Dislikes",
								value=0
							).add_field(
								name="\u200b",
								value="\u200b"
							).add_field(
								name="Account Information",
								value="<a:moving_gear:874897860469088296> Here is all of your account information! You can change it using p!set command!",
								inline=False
							).add_field(
								name="🫂 Gender",
								value=label
							).add_field(
								name="📧 email",
								value=email
							).add_field(
								name="🔑 Password",
								value="||Password Redacted||",
								inline=False
							).add_field(
								name="⌛ Account Age",
								value=f"<t:{int(age)}:F>"
							),
							components=[
								
							]
						)
						await inter.reply(
							ctx.author.mention,
							type=ResponseType.ChannelMessageWithSource, 
							embed=discord.Embed(
								title="Congratulation!",
								description=f"{ctx.author.mention}, your account was made! Please use the help command to see the help menu!",
								color=discord.Color.from_rgb(213, 240, 213)
							)
						)
						await cur.close()
						await cur2.close()
						await db.close()
						await db2.close()
						on_click.kill()

					@on_click.matching_id("red")
					async def _Red(inter):
						await inter.reply(
							embed=discord.Embed(
							description="Aborting",
							color=discord.Color.red()
						))
						on_click.kill()
					

					@on_click.timeout
					async def _on_timeout():
						await confirm.delete()
						await ctx.send(
							ctx.author.mention,
							embed=discord.Embed(
								title="Timeout!",
								description="I have stop the command due to its long activity!",
								color=discord.Color.red()
							)
						)
				
			
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

	
				

		@on_click.timeout
		async def on_timeout():
			await embed_message.delete()
			await ctx.send(
				ctx.author.mention,
				embed=discord.Embed(
					title="Timeout!",
					description="I have stop the command due to its long activity!",
					color=discord.Color.red()
				)
			)
		
		print("e")
		

		
	@commands.command("post",  description="Post a video!")
	async def _post(self, ctx):
		# if not ctx.author.id in self.bot.owner_ids:
		# 	await ctx.send(
		# 		embed=discord.Embed(
		# 			description="Post command is under renovation!",
		# 			color=discord.Color.red()
		# 		)
		# 	)
			
		# 	return

		try:
			cur=await helper.find_in_channel(ctx.author.id)
			if cur:
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
					return

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
				con=await helper.connect("db/channel.db")
				cur=await helper.cursor(con)
				await cur.execute("SELECT channel FROM channel WHERE member_id=?", (ctx.author.id,))
				source=await cur.fetchone()
				token=str(uuid4().int)[:10]
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


							await asyncio.sleep(0.5)
							await em.edit(content="Are you sure you want to post this video?\nClick the green button to post this video or click the red button to cancelled this process!", embed=discord.Embed(
								title=title.content,
								url=x,
								description=description if len(description) > 1 else "This video dont have a description",
								color=discord.Color.from_rgb(213, 240, 213)
							).set_footer(
								text=f"Source : @{source[0]} | Date: {datetime.datetime.utcnow().strftime('%m/%d/%Y')} | ID: {token}"
							).set_author(
								name=f"@{source[0]}",
								url=x,
								icon_url=ctx.author.avatar_url
							).set_image(
								url=x
							).add_field(
								name="<:likes:875659362343993404> Likes",
								value=0
							).add_field(
								name="🫂 Views",
								value=0
							).add_field(
								name="<:dislikes:875659362264309821> Dislikes",
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
										emoji="<:tick_no:874284510575996968>",
										custom_id="red"
										)
									)
								]
							)

							if x.content_type in ["video/mp4", "video/mp3"]:
								await ctx.send(x)

							on_click = em.create_click_listener(timeout=120.0) 
							
							@on_click.not_from_user(ctx.author, reset_timeout=True)
							async def on_wrong_user(inter):
								await inter.reply(
									embed=discord.Embed(
									description="You are not the member who use this command!",
									color=discord.Color.red()
								), 
									ephemeral=True
								)

							@on_click.matching_id("green")
							async def _green(inter):
								nonlocal token
								date_=int(time.time())
								con=await helper.connect("db/video.db")
								cur=await helper.cursor(con)
								await cur.execute("INSERT INTO video VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", (ctx.author.id, str(title.content), str(description), str(x), 0, 0, 0, f'["{ctx.author.id}"]', f'["{ctx.author.id}"]', x.content_type, date_, token, f'["{ctx.author.id}"]'))
								await con.commit()
								await cur.close()
								await con.close()

								con=await helper.connect("db/channel.db")
								cur=await helper.cursor(con)
								await cur.execute("SELECT videos FROM channel WHERE member_id=?", (ctx.author.id,))
								data=await cur.fetchone()
								data=int(data[0])
								data += 1
								await cur.execute("UPDATE channel SET videos = ? WHERE member_id=?", (data, ctx.author.id))
								await con.commit()
								await cur.close()
								await con.close()
								await inter.reply(
									content="Posted!",
									type=ResponseType.UpdateMessage, 
									embed=discord.Embed(
									title=title.content,
									url=x,
									description=description if len(description) > 1 else f"Posted date: <t:{date_}:d>",
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
										name="<:likes:875659362343993404> Likes",
										value=0
									).add_field(
										name="🫂 Views",
										value=0
									).add_field(
										name="<:dislikes:875659362264309821> Dislikes",
										value=0
									)
								)

								on_click.kill()

							@on_click.matching_id("red")
							async def _red(inter):
								await inter.reply(
									content="Declined!", 
									type=ResponseType.UpdateMessage,
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
											name="<:likes:875659362343993404> Likes",
											value=0
										).add_field(
											name="🫂 Views",
											value=0
										).add_field(
											name="<:dislikes:875659362264309821> Dislikes",
											value=0
										), 
									)
								on_click.kill()

							@on_click.timeout
							async def on_timeout():
								await em.delete()
								await ctx.send(
									ctx.author.mention,
									embed=discord.Embed(
										title="Timeout!",
										description="I have stop the command due to its long activity!",
										color=discord.Color.red()
									)
								)

				elif attach.content.startswith("http"):
					em=await ctx.send(embed=discord.Embed(
						title="Posting...",
						color=discord.Color.from_rgb(213, 240, 213)
					).set_footer(
						text="Might take a few seconds!"
					))

					await asyncio.sleep(0.5)
					await em.edit(content="Are you sure you want to post this video?\nClick the green button to post this video or click the red button to cancelled this process!", embed=discord.Embed(
						title=title.content,
						description=description if len(description) > 1 else "This video dont have a description",
						color=discord.Color.from_rgb(213, 240, 213)
					).set_footer(
						text=f"Source : @{source[0]} | Date: {datetime.datetime.utcnow().strftime('%m/%d/%Y')} | ID: {token}"
					).set_author(
						name=f"{ctx.author} (@{source[0]})",
						icon_url=ctx.author.avatar_url
					).add_field(
						name="<:likes:875659362343993404> Likes",
						value=0
					).add_field(
						name="🫂 Views",
						value=0
					).add_field(
						name="<:dislikes:875659362264309821> Dislikes",
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
									emoji="<:tick_no:874284510575996968>",
									custom_id="red"
								)
							)
						]
					)

					await ctx.send(attach.content)
					on_click = em.create_click_listener(timeout=120.0) 
							
					@on_click.not_from_user(ctx.author, reset_timeout=True)
					async def on_wrong_user(inter):
						await inter.reply(
							embed=discord.Embed(
							description="You are not the member who use this command!",
							color=discord.Color.red()
						), 
							ephemeral=True
						)

					@on_click.matching_id("green")
					async def _green(inter):
						nonlocal token

						date_=int(time.time())
						con=await helper.connect("db/video.db")
						cur=await helper.cursor(con)
						await cur.execute("INSERT INTO video VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", (ctx.author.id, str(title.content), str(description), str(attach.content), 0, 0, 0, f'["{ctx.author.id}"]', f'["{ctx.author.id}"]', "link", date_, token, f'["{ctx.author.id}"]'))
						await con.commit()
						await cur.close()
						await con.close()

						con=await helper.connect("db/channel.db")
						cur=await helper.cursor(con)
						await cur.execute("SELECT videos FROM channel WHERE member_id=?", (ctx.author.id,))
						data=await cur.fetchone()
						data=int(data[0])
						data += 1
						await cur.execute("UPDATE channel SET videos = ? WHERE member_id=?", (data, ctx.author.id))
						await con.commit()
						await cur.close()
						await con.close()
						
						await inter.reply(
							content="Posted!",
							type=ResponseType.UpdateMessage, 
							embed=discord.Embed(
							title=title.content,
							description=description if len(description) > 1 else "This video dont have a description",
							color=discord.Color.from_rgb(213, 240, 213)
							).set_footer(
								text=f"Source : @{source[0]} | Date: {datetime.datetime.utcnow().strftime('%m/%d/%Y')} | ID: {token}"
							).set_author(
								name=f"{ctx.author} (@{source[0]})",
								icon_url=ctx.author.avatar_url
							).add_field(
								name="<:likes:875659362343993404> Likes",
								value=0
							).add_field(
								name="🫂 Views",
								value=0
							).add_field(
								name="<:dislikes:875659362264309821> Dislikes",
								value=0
							)
						)
						
						on_click.kill()

					@on_click.matching_id("red")
					async def _red(inter):
						await inter.reply(
							content="Declined!", 
							type=ResponseType.UpdateMessage,
							embed=discord.Embed(
								title=title.content,
								description=description if len(description) > 1 else "This video dont have a description",
								color=discord.Color.from_rgb(213, 240, 213)
								).set_footer(
									text=f"Source : @{source[0]} | Date: {datetime.datetime.utcnow().strftime('%m/%d/%Y')} | ID: {token}"
								).set_author(
									name=f"{ctx.author} (@{source[0]})",
									icon_url=ctx.author.avatar_url
								).add_field(
									name="<:likes:875659362343993404> Likes",
									value=0
								).add_field(
									name="🫂 Views",
									value=0
								).add_field(
									name="<:dislikes:875659362264309821> Dislikes",
									value=0
								), 
							)
						on_click.kill()

					@on_click.timeout
					async def on_timeout():
						await em.delete()
						await ctx.send(
							ctx.author.mention,
							embed=discord.Embed(
								title="Timeout!",
								description="I have stop the command due to its long activity!",
								color=discord.Color.red()
							)
						)

				else:
					await ctx.send(embed=discord.Embed(\
						color=discord.Color.red()
					).set_footer(
						text="Please send an attachment next time, the attachment must be mp3/mp4/gif."
					))
			else:
				await ctx.send(embed=self.channel_error)
		
		except Exception as e:
			raise e from e

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
				msg=await ctx.send(
					embed=discord.Embed(
					title=data[i][1],
					url=data[i][3],
					description=data[i][2],
					color=discord.Color.from_rgb(213, 240, 213)
				).set_footer(
					text=f"Videos {i + 1}/{video} | Date: {date_time} | ID: {data[i][10]}",
					icon_url=channel_data[3]
				).set_author(
					name=f"{ctx.author.name} (@{channel_data[1]})",
					icon_url=channel_data[3]
				), components=[
						ActionRow(
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
								custom_id="view-button",
								disabled=True
							),
							Button(
								style=ButtonStyle.green,
								label=data[i][4],
								emoji="<:likes:875659362343993404>",
								custom_id="like-button",
								disabled=True
							),
							Button(
								style=ButtonStyle.red,
								label=data[i][5],
								emoji="<:dislikes:875659362264309821>",
								custom_id="dislike-button",
								disabled=True
							),
							Button(
								style=ButtonStyle.grey,
								label=date_time,
								emoji="\U0000231b",
								custom_id="time-button",
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
							page=0
							try:
								page=int(select.content)
							except ValueError:
								await asyncio.sleep(0.1)

							if page > video:
								await ctx.send("Number is Too large, enter it again with smaller one")
								await asyncio.sleep(0.5)
							
							elif page <= 0:
								await ctx.send("Number cannot be minus, zero, or letters enter it again with bigger one")
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
			raw_date=datetime.datetime.fromtimestamp(int(data[i][10]))
			date_time=raw_date.strftime("%m/%d/%Y")
			msg=await ctx.send(embed=discord.Embed(
				title=data[i][1],
				url=data[i][3],
				description=data[i][2],
				color=discord.Color.from_rgb(213, 240, 213)
			).set_footer(
				text=f"Video {i + 1}/{video} | Date: {date_time} | ID: {data[i][11]}",
				icon_url=channel_data[3]
			).set_author(
				name=f"{ctx.author.name} (@{channel_data[1]})",
				icon_url=channel_data[3]
			)
		)
			file=await ctx.send(
					data[i][3],
					components=[
						ActionRow(
							Button(
								style=ButtonStyle.blurple,
								label=data[i][4],
								emoji="\U0001f465",
								custom_id="view-button",
								disabled=True
							),
							Button(
								style=ButtonStyle.blurple,
								label=channel_data[4],
								emoji=discord.PartialEmoji(name="follow", id=875659362264309791, animated=False),
								custom_id="subs-button",
								disabled=True
							),
							Button(
								style=ButtonStyle.green,
								label=data[i][5],
								emoji="<:likes:875659362343993404>",
								custom_id="like-button",
								disabled=True
							),
							Button(
								style=ButtonStyle.red,
								label=data[i][6],
								emoji="<:dislikes:875659362264309821>",
								custom_id="dislike-button",
								disabled=True
							),
							Button(
								style=ButtonStyle.grey,
								label=date_time,
								emoji="\U0000231b",
								custom_id="time-button",
								disabled=True
							)
						)
					]
				)		

	@commands.command()
	@commands.is_owner()
	async def set_video(self, ctx):
		con=await helper.connect("db/channel.db")
		cur=await helper.cursor(con)

		await cur.execute("UPDATE channel SET views = 1 WHERE member_id = ?", (ctx.author.id,))


		await con.commit()
		await cur.close()
		await con.close()
			
	@commands.command("search", description="Search up videos that got posted by other members!")
	async def _search(self, ctx, *,name):
		loop=True
		if not len(name) >= 3:
			await ctx.send(embed=discord.Embed(
				color=discord.Color.red()
			).set_footer(
				text="The name argument must have 3 or more characters"
			))
			return

		videos=await helper.find_videos(name)
		data=[x for x in videos]
		
		
		i = 0
		if len(data) > 1:
			while True:
				channel_data=await helper.find_in_channel(data[i][8])
				con=await helper.connect("db/video.db")
				cur=await helper.cursor(con)
				con2=await helper.connect("db/channel.db")
				cur2=await helper.cursor(con2)
				videos=await helper.find_videos(name)
				data=[x for x in videos]
				try:
					if loop == True:
						old_views=ast.literal_eval(data[i][11])
						if not str(ctx.author.id) in old_views:
							old_views.append(str(ctx.author.id))
							await cur.execute("UPDATE video SET old_views = ? WHERE link = ?", (str(old_views), data[i][0]))
							await cur.execute("UPDATE video SET views = ? WHERE link = ?", (data[i][3] + 1 if int(data[i][8]) != ctx.author.id else data[i][3] + 0, data[i][0]))
							await cur2.execute("UPDATE channel SET views = ? WHERE member_id = ?", (channel_data[7] + 1, data[i][8]))
							
						
						raw_date=datetime.datetime.fromtimestamp(int(data[i][9]))
						date_time=raw_date.strftime("%m/%d/%Y")	
						num = i + 1
						user=await self.bot.fetch_user(channel_data[0])
						msg=await ctx.send(
							embed=discord.Embed(
								title=data[i][1],
								url=data[i][0],
								description=data[i][2],
								color=discord.Color.from_rgb(213, 240, 213)
							).set_footer(
								text=f"Videos {num}/{len(data)} | Date: {date_time} | ID: {data[i][10]}",
								icon_url=channel_data[3]
							).set_author(
								name=f"{user.name} (@{channel_data[1]})",
								icon_url=channel_data[3]
							),
							
							components=[
								ActionRow(
									Button(
										style=ButtonStyle.blurple,
										label="",
										emoji="\U00002b05",
										custom_id="left-button"
										
									),
									Button(
										style=ButtonStyle.red,
										label="",
										emoji="<:tick_no:874284510575996968>",
										custom_id="delete-button"
									),
									Button(
										style=ButtonStyle.blurple,
										label="",
										emoji="\U000027a1",
										custom_id="right-button"
									),
									Button(
										style=ButtonStyle.grey,
										label=date_time,
										emoji="\U0000231b",
										custom_id="time-button",
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
										style=ButtonStyle.blurple,
										label=data[i][3],
										emoji="\U0001f465",
										custom_id="view-button",
										disabled=True
									),
									Button(
										style=ButtonStyle.green,
										label=data[i][4],
										emoji="<:likes:875659362343993404>",
										custom_id="like-button",
										disabled=True if str(ctx.author.id) in ast.literal_eval(data[i][6]) else False
									),
									Button(
										style=ButtonStyle.red,
										label=data[i][5],
										emoji="<:dislikes:875659362264309821>",
										custom_id="dislike-button",
										disabled=True if str(ctx.author.id) in ast.literal_eval(data[i][7]) else False
									)
								)
							]
						)

						await con.commit()
						await con2.commit()

					while True:
						inter = await ctx.wait_for_button_click(lambda inter: inter.message.id == msg.id or inter.message.id == file.id and inter.channel == ctx.channel)	
						author=await helper.find_in_channel(inter.author.id)
						if author == None:
							await ctx.send(embed=self.channel_error)
							return
						
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
						loop = True
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

						await cur.close()
						await cur2.close()
						await con.close()
						await con2.close()

					elif button_id == "left-button": #Left Button
						loop = True
						if inter.author == ctx.author:
							i = (len(data) - 1)
							await msg.delete()
							await file.delete()
							await asyncio.sleep(0.5)
						
						else:
							i -= 1
							await msg.delete()
							await file.delete()
							await asyncio.sleep(0.5)
	
						await cur.close()
						await cur2.close()
						await con.close()
						await con2.close()

					elif button_id == "delete-button": #Delete Button
						await msg.delete()
						await file.delete()
						await ctx.send(embed=discord.Embed(
								description=f"{ctx.author.mention} thanks for using Tango bot :blush:",
								color=discord.Color.from_rgb(213, 240, 213),
							)
						)
						
						await cur.close()
						await cur2.close()
						await con.close()
						await con2.close()
						break

					elif button_id == "like-button": #Like Button
						likes=ast.literal_eval(data[i][6]) #list member who likes
						dislikes=ast.literal_eval(data[i][7]) #list member who dislikes
						await cur2.execute("UPDATE channel SET likes = ? WHERE member_id = ?", (channel_data[5] + 1, data[i][8]))


						if not str(ctx.author.id) in likes:
							likes.append(str(ctx.author.id))
							
			
						if str(ctx.author.id) in dislikes:
							dislikes.remove(str(ctx.author.id))
							await cur.execute("UPDATE video SET old_dislikes = ? WHERE link = ?", (str(dislikes), str(data[i][0])))
							await cur.execute("UPDATE video SET dislikes = ? WHERE link = ?", (data[i][5] - 1, str(data[i][0])))
							await cur2.execute("UPDATE channel SET dislikes = ? WHERE member_id = ?", (channel_data[6] - 1, data[i][8]))
						
						
						await cur.execute("UPDATE video SET old_likes = ? WHERE link = ?", (str(likes), str(data[i][0])))
						await cur.execute("UPDATE video SET likes = ? WHERE link = ?", (int(data[i][4]) + 1, str(data[i][0])))

						await con.commit()
						await con2.commit()

						await inter.send(embed=discord.Embed(
							description=f"{ctx.author.mention} Liked this video!",
							color=discord.Color.from_rgb(213, 240, 213)
						),
							ephemeral=True
						)

						await file.edit(
							content=data[i][0],
							components=[
								ActionRow(
									Button(
										style=ButtonStyle.blurple,
										label=data[i][3],
										emoji="\U0001f465",
										custom_id="view-button",
										disabled=True
									),
									Button(
										style=ButtonStyle.green,
										label=data[i][4] + 1,
										emoji="<:likes:875659362343993404>",
										custom_id="like-button",
										disabled=True
									),
									Button(
										style=ButtonStyle.red,
										label=data[i][5] - 1 if str(ctx.author.id) in ast.literal_eval(data[i][7]) else data[i][5],
										emoji="<:dislikes:875659362264309821>",
										custom_id="dislike-button",
										disabled=False
									)
								)
							]
						)
						
						loop = False
						await cur.close()
						await cur2.close()
						await con.close()
						await con2.close()
								
					elif button_id == "dislike-button": #Dislike Button
						likes=ast.literal_eval(data[i][6])
						dislikes=ast.literal_eval(data[i][7])
						await cur2.execute("UPDATE channel SET dislikes = ? WHERE member_id = ?", (channel_data[6] + 1, data[i][8]))

						if not str(ctx.author.id) in dislikes:
							dislikes.append(str(ctx.author.id))
							
						if str(ctx.author.id) in likes:
							likes.remove(str(ctx.author.id))
							await cur.execute("UPDATE video SET old_likes = ? WHERE link = ?", (str(likes), str(data[i][0])))
							await cur.execute("UPDATE video SET likes = ? WHERE link = ?", (data[i][4] - 1, str(data[i][0])))
							await cur2.execute("UPDATE channel SET likes = ? WHERE member_id = ?", (channel_data[5] - 1, data[i][8]))
						
						
						
						await cur.execute("UPDATE video SET old_dislikes = ? WHERE link = ?", (str(dislikes), str(data[i][0])))
						await cur.execute("UPDATE video SET dislikes = ? WHERE link = ?", (int(data[i][5]) + 1, str(data[i][0])))
						
						
						await con.commit()
						await con2.commit()

						await inter.send(embed=discord.Embed(
							description=f"{ctx.author.mention} Disliked this video!",
							color=discord.Color.from_rgb(213, 240, 213)
						),
							ephemeral=True
						)
						
						await file.edit(
							content=data[i][0],
							components=[
								ActionRow(
									Button(
										style=ButtonStyle.blurple,
										label=data[i][3],
										emoji="\U0001f465",
										custom_id="view-button",
										disabled=True
									),
									Button(
										style=ButtonStyle.green,
										label=data[i][4] - 1 if str(ctx.author.id) in ast.literal_eval(data[i][6]) else data[i][4],
										emoji="<:likes:875659362343993404>",
										custom_id="like-button",
										disabled=False
									),
									Button(
										style=ButtonStyle.red,
										label=data[i][5] + 1,
										emoji="<:dislikes:875659362264309821>",
										custom_id="dislike-button",
										disabled=True
									)
								)
							]
						)
						loop = False
						await cur.close()
						await cur2.close()
						await con.close()
						await con2.close()

				except Exception as e:
					raise e




		elif len(data) == 1:
			while True:
				channel_data=await helper.find_in_channel(data[i][8])
				con=await helper.connect("db/video.db")
				cur=await helper.cursor(con)
				con2=await helper.connect("db/channel.db")
				cur2=await helper.cursor(con2)
				videos=await helper.find_videos(name)
				data=[x for x in videos]
				print(data)
				if loop == True:
					old_views=ast.literal_eval(data[i][11])
					if not str(ctx.author.id) in old_views:
						old_views.append(str(ctx.author.id))
						await cur.execute("UPDATE video SET old_views = ? WHERE link = ?", (str(old_views), data[i][0]))
						await cur.execute("UPDATE video SET views = ? WHERE link = ?", (data[i][3] + 1 if int(data[i][8]) != ctx.author.id else data[i][3] + 0, data[i][0]))
						await cur2.execute("UPDATE channel SET views = ? WHERE member_id = ?", (channel_data[7] + 1, data[i][8]))
					
					raw_date=datetime.datetime.fromtimestamp(int(data[i][9]))
					date_time=raw_date.strftime("%m/%d/%Y")
					msg=await ctx.send(
						embed=discord.Embed(
							title=data[i][1],
							url=data[i][0],
							description=data[i][2],
							color=discord.Color.from_rgb(213, 240, 213)
						).set_footer(
							text=f"Videos 1/1 | Date: {date_time} | ID: {data[i][10]}"
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
									emoji="<:tick_no:874284510575996968>",
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
									style=ButtonStyle.blurple,
									label=data[i][3],
									emoji="\U0001f465",
									custom_id="view-button",
									disabled=True
								),
								Button(
									style=ButtonStyle.green,
									label=data[i][4],
									emoji="<:likes:875659362343993404>",
									custom_id="like-button",
									disabled=True if str(ctx.author.id) in data[i][6] else False
								),
								Button(
									style=ButtonStyle.red,
									label=data[i][5],
									emoji="<:dislikes:875659362264309821>",
									custom_id="dislike-button",
									disabled=True if str(ctx.author.id) in data[i][7] else False
								),
								Button(
									style=ButtonStyle.grey,
									label=date_time,
									emoji="\U0000231b",
									custom_id="time-button",
									disabled=True
								)
							)
						]
					)

					
					
					await con.commit()
					await con2.commit()
				
			
				try:
					while True:
						inter = await ctx.wait_for_button_click(lambda inter: inter.message.id == msg.id or inter.message.id == file.id and inter.channel == ctx.channel)
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

					if button_id == "delete-button": #Delete Button
						await msg.delete()
						await file.delete()
						await ctx.send(embed=discord.Embed(
								description=f"{ctx.author.mention} thanks for using Tango bot :blush:",
								color=discord.Color.from_rgb(213, 240, 213),

							)
						)

						await cur.close()
						await cur2.close()
						await con.close()
						await con2.close()
						break

					elif button_id == "like-button": #Like Button
						likes=ast.literal_eval(data[i][6]) #list member who likes
						dislikes=ast.literal_eval(data[i][7]) #list member who dislikes
		
						if not str(ctx.author.id) in likes:
							likes.append(str(ctx.author.id))
							await cur2.execute("UPDATE channel SET likes = ? WHERE member_id = ?", (channel_data[5] + 1, data[i][8]))
			
						if str(ctx.author.id) in dislikes:
							dislikes.remove(str(ctx.author.id))
							await cur.execute("UPDATE video SET old_dislikes = ? WHERE link = ?", (str(dislikes), str(data[i][0])))
							await cur.execute("UPDATE video SET dislikes = ? WHERE link = ?", (data[i][5] - 1, str(data[i][0])))
							await cur2.execute("UPDATE channel SET dislikes = ? WHERE member_id = ?", (channel_data[6] - 1, data[i][8]))
						
						
						await cur.execute("UPDATE video SET old_likes = ? WHERE link = ?", (str(likes), str(data[i][0])))
						await cur.execute("UPDATE video SET likes = ? WHERE link = ?", (int(data[i][4]) + 1, str(data[i][0])))

						await con.commit()
						await con2.commit()

						await inter.send(embed=discord.Embed(
							description=f"{ctx.author.mention} Liked this video!",
							color=discord.Color.from_rgb(213, 240, 213)
						),
							ephemeral=True
						)

						await file.edit(
							content=data[i][0],
							components=[
								ActionRow(
									Button(
										style=ButtonStyle.blurple,
										label=data[i][3],
										emoji="\U0001f465",
										custom_id="view-button",
										disabled=True
									),
									Button(
										style=ButtonStyle.green,
										label=data[i][4] + 1,
										emoji="<:likes:875659362343993404>",
										custom_id="like-button",
										disabled=True
									),
									Button(
										style=ButtonStyle.red,
										label=data[i][5] - 1 if str(ctx.author.id) in ast.literal_eval(data[i][7]) else data[i][5],
										emoji="<:dislikes:875659362264309821>",
										custom_id="dislike-button",
										disabled=False
									)
								)
							]
						)
						
						loop = False
						await cur.close()
						await cur2.close()
						await con.close()
						await con2.close()
						
								
					elif button_id == "dislike-button": #Dislike Button
						likes=ast.literal_eval(data[i][6])
						dislikes=ast.literal_eval(data[i][7])
						
						if not str(ctx.author.id) in dislikes:
							dislikes.append(str(ctx.author.id))
							await cur2.execute("UPDATE channel SET dislikes = ? WHERE member_id = ?", (channel_data[6] + 1, data[i][8]))

						if str(ctx.author.id) in likes:
							likes.remove(str(ctx.author.id))
							await cur.execute("UPDATE video SET old_likes = ? WHERE link = ?", (str(likes), str(data[i][0])))
							await cur.execute("UPDATE video SET likes = ? WHERE link = ?", (data[i][4] - 1, str(data[i][0])))
							await cur2.execute("UPDATE channel SET likes = ? WHERE member_id = ?", (channel_data[5] - 1, data[i][8]))
						
						
						
						await cur.execute("UPDATE video SET old_dislikes = ? WHERE link = ?", (str(dislikes), str(data[i][0])))
						await cur.execute("UPDATE video SET dislikes = ? WHERE link = ?", (int(data[i][5]) + 1, str(data[i][0])))
						
						await con.commit()
						await con2.commit()

						await inter.send(embed=discord.Embed(
							description=f"{ctx.author.mention} Disliked this video!",
							color=discord.Color.from_rgb(213, 240, 213)
						),
							ephemeral=True
						)
						
						await file.edit(
							content=data[i][0],
							components=[
								ActionRow(
									Button(
										style=ButtonStyle.blurple,
										label=data[i][3],
										emoji="\U0001f465",
										custom_id="view-button",
										disabled=True
									),
									Button(
										style=ButtonStyle.green,
										label=data[i][4] - 1 if str(ctx.author.id) in ast.literal_eval(data[i][6]) else data[i][4],
										emoji="<:likes:875659362343993404>",
										custom_id="like-button",
										disabled=False
									),
									Button(
										style=ButtonStyle.red,
										label=data[i][5] + 1,
										emoji="<:dislikes:875659362264309821>",
										custom_id="dislike-button",
										disabled=True
									)
								)
							]
						)
						loop = False
						await cur.close()
						await cur2.close()
						await con.close()
						await con2.close()

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
			title="<a:moving_gear:874897860469088296> Setting Menu",
			description="Is there anything i could help?",
			color=discord.Color.from_rgb(213, 240, 213)
		), 
		components=[
				SelectMenu(
					custom_id="Option",
					placeholder="Choose your change",
					max_values=1,
					options=[
						SelectOption("Channel Name", "channel", description="Set a new channel name!", emoji="\U0001f4db"),
						SelectOption("Channel Description", "description", description="Set a new channel description. Need to set limit later!", emoji="\U0001f6d1"),
						SelectOption("Channel Banner", "banner", description="Set a new channel banner!", emoji="\U0001f5bc"),
						SelectOption("User Gender", "gender", description="Set your new gender!", emoji="\U00002642"),
						SelectOption("User email", "email", description="Set your new email. Must not have special characters\nMust be a minimum of 5 to 13 characters", emoji="\U0001f4e7"),
						SelectOption("User Password", "password", description="Set your new password. Must not have special characters\nMust be a minimum of 5 to 13 characters", emoji="\U0001f6c2")

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
					description=f"Type your new {label}! Must not have special characters and Must be minimum of 5 to 13 characters",
					color=discord.Color.from_rgb(213, 240, 213)
				).set_footer(
					text="You have 120 seconds to do this"
				))
				msg=await self.bot.wait_for("message", check=lambda x: x.author == ctx.author and x.channel == ctx.channel, timeout=120)
				await cur.execute("UPDATE channel SET channel = ? WHERE member_id = ?", (msg.content, ctx.author.id))
				await ctx.send(embed=discord.Embed(
						description="Done! Check it using p!profile",
						color=discord.Color.from_rgb(213, 240, 213)
					)
				)
				await db.commit()
				await cur.close()

			elif value == "description":
				await inter.reply(embed=discord.Embed(
					title="Type your change",
					description=f"Type your new {label}!",
					color=discord.Color.from_rgb(213, 240, 213)
				).set_footer(
					text="You have 120 seconds to do this"
				))
				msg=await self.bot.wait_for("message", check=lambda x: x.author == ctx.author and x.channel == ctx.channel, timeout=120)
				await cur.execute("UPDATE channel SET description = ? WHERE member_id = ?", (msg.content, ctx.author.id))
				await ctx.send(embed=discord.Embed(
						description="Done! Check it using p!profile",
						color=discord.Color.from_rgb(213, 240, 213)
					)
				)
				
				await db.commit()
				await cur.close()

			elif value == "banner":
				await inter.reply(embed=discord.Embed(
					title="Type your change",
					description=f"Type your new {label}!\nThe link must be an https link, mp4, mp3, gif, png, jpg, or webp!",
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
									description="Done! Check it using p!profile",
									color=discord.Color.from_rgb(213, 240, 213)
								)
							)
							break
						
					else:
						await cur.execute("UPDATE channel SET banner = ? WHERE member_id = ?", (msg.content, ctx.author.id))
						await ctx.send(embed=discord.Embed(
								description="Done! Check it using p!profile",
								color=discord.Color.from_rgb(213, 240, 213)
							)
						)
						
				await db.commit()
				await cur.close()
			
	#=================================================

			elif value == "gender":
				Message=await inter.reply(embed=discord.Embed(
					title="Select your change",
					description="Select your new Gender!",
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
				gender = await Message.wait_for_dropdown(check=lambda inter: inter.author == ctx.author)
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
					description=f"Type your new email! (e.g EpicUser123, EpicDiscord123)\nMust not have special characters and Must be minimum of 5 to 13 characters",
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
						description="Done! Check it using p!profile",
						color=discord.Color.from_rgb(213, 240, 213)
					)
				)

				await db2.commit()
				await info.close()

			elif value == "password":
				await inter.reply(f"{ctx.author.mention} check your DM")
				await ctx.author.send(embed=discord.Embed(
					title="Type your change",
					description=f"Type your new Password! Must not have special characters and Must be minimum of 5 to 13 characters",
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

		finally:
			await db.close()
			await db2.close()

def setup(bot):
	bot.add_cog(Social(bot))