import discord
import asyncio
import helper
import time
import datetime
import ast
import requests
import base64

#=============================== 

from uuid import uuid4
from discord.ext import commands
from dislash import InteractionClient, ActionRow, Button, ButtonStyle, SelectMenu, SelectOption, ResponseType

class social(commands.Cog):
	"""Social is a group of commands that contain most of the commands that other can use ;)"""
	def __init__(self, bot):
		self.bot = bot
		self.embed_color=discord.Color.from_rgb(136, 223 ,251)
		self.special_characters = ["!", "”", "#", "$", "%", "&", "’", ")", "(", "*", "+", ",", "-", ".", "/", ":", ";", "<", "=", ">", "?", "@", "[", "\\", "^", ">", "{", "}", "~", "`", " "]
		self.channel_error = discord.Embed(
			description="You haven't made your channel, Use `p!start` command!",
			color=discord.Color.red()
		)

		self.video_error = discord.Embed(
			color=discord.Color.red()
		).set_footer(
			text="You havent made a video, use p!upload command!"
		)

		self.login_error=discord.Embed(
			description="Use `p!login` command to login to you your account!",
			color=discord.Color.red()
		)
	

	@commands.command("profile", description="Profile command can let you see your channel stats!")
	@commands.cooldown(1, 5, commands.BucketType.user)
	async def _profile(self, ctx):
		data=await helper.find_in_channel(ctx.author.id)
		info=await helper.find_in_info(ctx.author.id)

		if not data or not info:
			await ctx.send(embed=self.channel_error)
			return

		if info[2] == 'no':
			await ctx.send(embed=self.login_error)
			return

		await ctx.send(
			embed=discord.Embed(
				title="Profile Menu!",
				description=data[2],
				color=self.embed_color,
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
						value="Here is all of your account information! You can change it using p!setting command!",
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
	@commands.cooldown(1, 5, commands.BucketType.user)
	async def _start(self, ctx):
		# if not ctx.author.id in self.bot.owner_ids:
		# 	await ctx.send("This cmd is other renovation")
		# 	return

		age=time.time()
		db=await helper.connect("db/channel.db")
		db2=await helper.connect("db/info.db")
		cur=await helper.cursor(db)	
		cur2=await helper.cursor(db2) 
		channel_data=await helper.find_in_channel(ctx.author.id)
		info=await helper.find_in_info(ctx.author.id)

		buttons = ActionRow(
			Button(
				style=ButtonStyle.green,
				label="Continue",
				emoji="<:tick_yes:874284510135607350>",
				custom_id="green"
			),
			Button(
				style=ButtonStyle.red,
				label="Abort",
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

		if info and info[2] == 'no':
			await ctx.send(embed=self.login_error)
			return

		embed_message=await ctx.send(embed=discord.Embed(
			title="Time to get start!!",
			description="Hello There 👋\nYou have 1 to 5 steps to make your TangoBot account, you can always press abort button to cancel the command! Click the green button to continues or click red button to cancel this command. The bot will guide you through the rest",
			color=self.embed_color
		).set_footer(
			text=f"{ctx.author} • Click the abort button cancel this command!",
			icon_url=ctx.author.avatar_url
		), components=[
				buttons
			]
		)
		
		while True:
			try:
				inter = await ctx.wait_for_button_click(lambda inter: inter.author == ctx.author and inter.channel == ctx.channel and inter.message == embed_message, timeout=20)	
				
				if inter.author != ctx.author:
					await inter.reply(embed=discord.Embed(
						description="You are not the member who use this command!",
						color=discord.Color.red()
					), 
						ephemeral=True
					)
					
				else:
					break

			except asyncio.TimeoutError:
				await embed_message.delete()
				await ctx.send(embed=discord.Embed(
					title="Timeout!",
					description="I have stop the command due to its long activity!",
					color=discord.Color.red()
				))
				return

		try:
			#Channel Name 
			message=await embed_message.edit(
				embed=discord.Embed(
				title="Step 1",
				description="Type your channel name. This name will get displayed in your profile and whenever someone check your channel display.",
				color=self.embed_color
			).add_field(
				name="Requirements!",
				value="\> Type your channel name without any special characters!\n\> Minimum of 5 to 15 characters!\n\> Make sure the name is not exist yet."
			).set_footer(
				text=f"{ctx.author} • You can type abort to cancel this command!",
				icon_url=ctx.author.avatar_url
			), components=[
				
			])
				
			msg=await self.bot.wait_for("message", check=lambda x: x.author == ctx.author and x.channel == ctx.channel, timeout=25)
			
			if msg.content.lower() == "abort":
				await embed_message.delete()
				await ctx.send(embed=discord.Embed(
					description="Aborting...",
					color=discord.Color.red()
				))
				return

			for x in self.special_characters:
				if x in msg.content:
					await ctx.send(embed=discord.Embed(
						description="Dont put special characters in channel name!",
						color=discord.Color.red()
					))
					return 

			if len(msg.content) > 15 or len(msg.content) < 5:
				await ctx.send(embed=discord.Embed(
					description="You put too much or too little characters!",
					color=discord.Color.red()
				))
				return

			await cur.execute("SELECT member_id FROM channel WHERE channel = ?", (msg.content,))
			acc=await cur.fetchone()

			if acc != None:
				await ctx.send(embed=discord.Embed(
					description="That name is already available! next time enter a different name!",
					color=discord.Color.red()
				))
				return
			
			#Select Gender
			await embed_message.edit(
				embed=discord.Embed(
				title="Step 2",
				description="Select your gender with the dropdown below this embed! This is only for info and will get display in your profile only!",
				color=self.embed_color
			).add_field(
				name="Requirements!",
				value="\> Select only one!\n\> You cant skip this process\n\> You may or may not use your real gender, it wont affect anything."
			).set_footer(
				text=f"{ctx.author} • You cant type abort in this process",
				icon_url=ctx.author.avatar_url
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
				try:
					inter = await embed_message.wait_for_dropdown(check=lambda interaction: interaction.author == ctx.author and interaction.message == embed_message, timeout=25)
					if inter.author != ctx.author:
						await inter.reply(embed=discord.Embed(
							description="You are not the member who use this command!",
							color=discord.Color.red()
						), 
							ephemeral=True
						)
						
					
					else:
						break

				except asyncio.TimeoutError:
					await ctx.send(embed=discord.Embed(
						title="Timeout",
						description="I have stop the command due to its long activity!",
						color=discord.Color.red()
					))
					return
				
			label = "".join([option.label for option in inter.select_menu.selected_options])
			await inter.reply(f"You choose **{label}**")
			await asyncio.sleep(2)

			#Select email
			await embed_message.edit(
				embed=discord.Embed(
				title="Step 3",
				description="Enter your email name, This step is very important because you need email to login to your account! Also in this step you dont need to send a real one! just enter a fake one of course with silly name.",
				color=self.embed_color
			).add_field(
				name="Requirements!",
				value="\> Type your email name without any special characters! Except Underscore(_)\n\> Minimum of 5 to 15 characters!\n\> Make sure the name is not exist yet.\n\> You may not use '@email' or similar word in this process!"
			).add_field(
				name="Example!",
				value="\> EpicUser123\n\> DiscordUser321",
				inline=True
			).set_footer(
				text=f"{ctx.author} • You can type abort to cancel this command!",
				icon_url=ctx.author.avatar_url
			),  components=[])

			email=await self.bot.wait_for("message", check=lambda x: x.author == ctx.author and x.channel == ctx.channel)

			if email.content.lower() == "abort":
				await embed_message.delete()
				await embed_message.edit(
					embed=discord.Embed(
						description="Aborting...",
						color=discord.Color.red()
			))	
				return

			for x in self.special_characters:
				if x in email.content:
					await embed_message.delete()
					await ctx.send(embed=discord.Embed(
						description="Dont put special characters in email name!",
						color=discord.Color.red()
					))
					return 

			if len(email.content) > 15 or len(email.content) < 5:
				await embed_message.delete()
				await ctx.send(embed=discord.Embed(
					description="You put too much or too little characters!",
					color=discord.Color.red()
				))
				return

			email=f"{email.content}@email.com"
			
			await cur2.execute("SELECT member_id FROM info WHERE email = ?", (email,))
			acc=await cur.fetchone()
			
			if acc:
				await ctx.send(embed=discord.Embed(
					description="That email is already available! next time enter a different name!",
					color=discord.Color.red()
				))
				return

			await ctx.send(f"Your email is {email}")
			await asyncio.sleep(2)

			#Select Password
			await ctx.send(f"{ctx.author.mention} Check your DM!")
			await ctx.author.send(embed=discord.Embed(
				title="Step 4",
				description="DM me your password! You need a minimum of 5 to 15 characters",
				color=self.embed_color
			).add_field(
				name="Requirements!",
				value="\> Type your password without any special characters! Except Underscore(_)\n\> Minimum of 5 to 15 characters!\n"
			).set_footer(
				text=f"{ctx.author} • You can type abort to cancel this command!",
				icon_url=ctx.author.avatar_url
			))

			password=await self.bot.wait_for("message", check=lambda x: x.author == ctx.author and isinstance(x.channel, discord.DMChannel), timeout=60)
			
			if password.content.lower() == "abort":
				await embed_message.delete()
				await ctx.author.send(
					embed=discord.Embed(
						description="Aborting...",
						color=discord.Color.red()
			))	
				return

			for x in self.special_characters:
				if x in password.content:
					await embed_message.delete()
					await ctx.author.send(embed=discord.Embed(
						description="Dont put special characters in password!",
						color=discord.Color.red()
					))
					return

			if len(password.content) > 15 or len(password.content) < 5:
				await embed_message.delete()
				await ctx.author.send(embed=discord.Embed(
					description="You put too much or too little characters!",
					color=discord.Color.red()
				))
				return 

			await ctx.author.send(f"Your password is ||{password.content}|| Continue to {ctx.channel.mention}!")

			confirm=await ctx.reply(
				f"**`Little bit more!`**\n{ctx.author.mention} You just need to confirm all of your credentials. We(TangoBot devs) respect all of your privacy, For your information we are only gonna store your Member-ID and your Tango bot account password which is bind to your ID!\nPlease click the green button to continue or the red button to decline this!",
				embed=discord.Embed(
				title="<a:moving_gear:874897860469088296> Profile",
				description="<a:moving_gear:874897860469088296> Set a new description, banner, using p!setting command! also you can change channel name, email, password, and gender so dont you worry!",
				color=self.embed_color,
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
				value="<a:moving_gear:874897860469088296> Here is all of your account information! You can change it using p!setting command!",
				inline=False
			).add_field(
				name="🫂 Gender",
				value=label
			).add_field(
				name="📧 email",
				value=email
			).add_field(
				name="🔑 Password",
				value="||[Password Redacted]||",
				inline=False
			).add_field(
				name="⌛ Account Age",
				value=f"<t:{int(age)}:F>"
			),
			components=[
				buttons
			]
		)
			on_click=confirm.create_click_listener(timeout=60.0)
			
			@on_click.not_from_user(ctx.author, cancel_others=True)
			async def _not_From_user(inter):
				await inter.reply(
					embed=discord.Embed(
						description="You are not the member who use this command!",
						color=discord.Color.red()
					), 
						ephemeral=True
					)

			@on_click.matching_id("green")
			async def _Green(inter):
				nonlocal password

				byt=bytes(password.content, encoding="UTF-8")
				password=base64.b64encode(byt).decode()
				await cur.execute("INSERT INTO channel VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", (ctx.author.id, msg.content, "Set a new description, banner, using p!setting command! also you can change channel name, email, password, and gender so dont you worry!", str(ctx.author.avatar_url), 0, 0, 0, 0, 0, "no", 0, f'["{ctx.author.id}"]'))
				await cur2.execute("INSERT INTO info VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", (ctx.author.id, label, "no", email, password, f"<t:{int(age)}:F>", '[]', '[]', '[]', '[]'))
				await db.commit()
				await db2.commit()
				await inter.reply(
					"",
					type=7,
					embed=discord.Embed(
						title="<a:moving_gear:874897860469088296> Profile",
						description="<a:moving_gear:874897860469088296> Set a new description, banner, using p!setting command! also you can change channel name, email, password, and gender so dont you worry!",
						color=self.embed_color,
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
						value="<a:moving_gear:874897860469088296> Here is all of your account information! You can change it using p!setting command!",
						inline=False
					).add_field(
						name="🫂 Gender",
						value=label
					).add_field(
						name="📧 email",
						value=email
					).add_field(
						name="🔑 Password",
						value="||[Password Redacted]||",
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
					embed=discord.Embed(
						title="Congratulation!",
						description=f"You made your account! Now use the `p!login` command to get access to your account!",
						color=self.embed_color
					)
				)
				await cur.close()
				await cur2.close()
				await db.close()
				await db2.close()
				on_click.kill()

			@on_click.matching_id("red")
			async def _Red(inter):
				await message.delete()
				await inter.reply(
					type=7,
					content="Aborting...",
					embed=discord.Embed(
					description="Aborting...",
					color=discord.Color.red()
				),  components=[])
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
		
	
		except asyncio.TimeoutError:
			await ctx.send(embed=discord.Embed(
				title="Timeout!",
				color=discord.Color.red()
			).set_footer(
				text="You are too slow, Use the command again!"
			))

	@commands.command("upload",  description="Upload a video!", aliases=['post', "up"])
	@commands.cooldown(1, 5, commands.BucketType.user)
	async def _upload(self, ctx):

		# if not ctx.author.id in self.bot.owner_ids:
		# 	await ctx.send(
		# 		embed=discord.Embed(
		# 			description="Post command is under renovation!",
		# 			color=discord.Color.red()
		# 		)
		# 	)
			
		# 	return
		info = await helper.find_in_info(ctx.author.id)
		acc=await helper.find_in_channel(ctx.author.id)
		 
		if not acc or not info:
			await ctx.send(embed=self.channel_error)
			return

		
		if info[2] == 'no':
			await ctx.send(embed=self.login_error)
			return
		try:
			cur=await helper.find_in_channel(ctx.author.id)
			if cur:
				await ctx.send(embed=discord.Embed(
					title="Title?",
					description="Type your video title! video title with get display in the title side of embed! Make sure its short and sweet!",
					color=self.embed_color
				).add_field(
					name="Requirements!",
					value="\> Must be between 4 to 100 characters!\n\> Type your title without any special characters! Except Underscore(_)"
				).set_footer(
					text=f"{ctx.author} • You cant type abort in this process",
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
				try:
					if title.attachments or requests.get(title.content).status_code <= 200:
						await ctx.send(embed=discord.Embed(
							description="Dont put attachments or url in title",
							color=discord.Color.red()
						))
						return
				except:
					pass

				await ctx.send(embed=discord.Embed(
					title="Description?",
					description="Type your video Description! if you dont want to include a description just enter a dot(.)",
					color=self.embed_color
				).add_field(
					name="Requirements!",
					value="\> Must be between 1 to 256 characters!"
				).set_footer(
					text=f"{ctx.author} • You cant type abort in this process",
					icon_url=ctx.author.avatar_url
				)
			)

				descriptions=await self.bot.wait_for("message", check=lambda x: x.author == ctx.author and x.channel == ctx.channel, timeout=120.0)
				description=descriptions.content

				try:
					if descriptions.attachments or requests.get(description.content).status_code <= 200:
						await ctx.send(embed=discord.Embed(
							description="Dont put attachments or url in description",
							color=discord.Color.red()
						))
						return
				except:
					pass

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
					title="Nsfw?",
					description="Is your video nsfw? type `y` if it is else `n`. This is an important step because it make sure that the video is obbeying discord ToS and guidelines. You will be blacklist if you upload nsfw video and didnt set this part to `y` !!",
					color=self.embed_color,
				).add_field(
					name="Requirements!",
					value="\> Your response must be either y or n!\n\> Make sure to type `y` if its nsfw video! if not then we will blacklist you!"
				).set_footer(
					text=f"{ctx.author} • You cant type abort in this process",
					icon_url=ctx.author.avatar_url
				)
			)

				nsfw=await self.bot.wait_for("message", check=lambda msg: msg.author == ctx.author and msg.channel == ctx.channel, timeout=120.0)
				
				if not nsfw.content.lower() in ['y', 'n']:
					await ctx.send(embed=discord.Embed(
						description=f"You need to enter `y` or `n`. Not {nsfw.content}",
						color=discord.Color.red()
					))
					return
				
				elif nsfw.content.lower() == 'y' and not nsfw.channel.is_nsfw():
					await ctx.send(embed=discord.Embed(
						description="You can only post nsfw video in nsfw channels!",
						color=discord.Color.red()
					))
					return

				await ctx.send(embed=discord.Embed(
					title="Attachment?",
					description="Send us one of your amazing video! Make sure its either mp4/mp3/gif or link such as tennor or giphy!",
					color=self.embed_color
				).add_field(
					name="Requirements!",
					value="\> Your response must be an attachment or link that we support!\n\> Dont send your attachment in a spoiler!\n\> Send only one attachment or link!"
				).set_footer(
					text=f"{ctx.author} • You cant type abort in this process",
					icon_url=ctx.author.avatar_url
				)
			)

				attach=await self.bot.wait_for("message", check=lambda x: x.author == ctx.author and x.channel == ctx.channel, timeout=120.0)
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
								color=self.embed_color
							).set_footer(
								text="Might take a few seconds!"
							))


							await asyncio.sleep(0.5)
							await em.edit(content="Are you sure you want to upload this video?\nClick the green button to upload this video or click the red button to cancelled this process!", embed=discord.Embed(
								title=title.content,
								url=x,
								description=description if len(description) > 1 else "",
								color=self.embed_color
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
										label="Continue",
										emoji="<:tick_yes:875659362117488671>",
										custom_id="green"
									),
									Button(
										style=ButtonStyle.red,
										label="Abort",				
										emoji="<:tick_no:874284510575996968>",
										custom_id="red"
										)
									)
								]
							)

							if x.content_type in ["video/mp4", "video/mp3"]:
								await ctx.send(x)

							on_click = em.create_click_listener(timeout=60.0) 
							
							@on_click.not_from_user(ctx.author, cancel_others=True, reset_timeout=True)
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
								nonlocal on_click

								date_=int(time.time())
								raw_date=datetime.datetime.fromtimestamp(date_)
								date_time=raw_date.strftime("%m/%d/%Y")
								con=await helper.connect("db/video.db")
								cur=await helper.cursor(con)
								await cur.execute("INSERT INTO video VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", (ctx.author.id, str(title.content), str(description), str(x), 0, 0, 0, f'["{ctx.author.id}"]', f'["{ctx.author.id}"]', x.content_type, date_, token, f'["{ctx.author.id}"]', "n", nsfw.content, 0))
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
									description=description if len(description) > 1 else "",
									color=self.embed_color
									).set_footer(
										text=f"Source : @{source[0]} | Date: {date_time} | ID: {token}"
									).set_author(
										name=f"{ctx.author.name} (@{source[0]})",
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
								nonlocal on_click

								await inter.reply(
									content="Declined!", 
									type=ResponseType.UpdateMessage,
									embed=discord.Embed(
										title=title.content,
										url=x,
										description=description if len(description) > 1 else "",
										color=self.embed_color
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
					tenor="tenor.com" in attach.content
					giphy="giphy.com" in attach.content
					
					
					if tenor is False and giphy is False:
						await ctx.send(embed=discord.Embed(
								color=discord.Color.red()
							).set_footer(
								text="We dont support that url/attachments at the moment!"
						))	
						return

					em=await ctx.send(embed=discord.Embed(
						title="Posting...",
						color=self.embed_color
					).set_footer(
						text="Might take a few seconds!"
					))

					await asyncio.sleep(0.5)
					await em.edit(content="Are you sure you want to upload this video?\nClick the green button to upload this video or click the red button to cancelled this process!", embed=discord.Embed(
						title=title.content,
						description=description if len(description) > 1 else "This video dont have a description",
						color=self.embed_color
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
									label="Continue",
									emoji="<:tick_yes:875659362117488671>",
									custom_id="green"
								),
								Button(
									style=ButtonStyle.red,
									label="Abort",
									emoji="<:tick_no:874284510575996968>",
									custom_id="red"
								)
							)
						]
					)

					await ctx.send(attach.content)
					on_click = em.create_click_listener(timeout=60.0) 
							
					@on_click.not_from_user(ctx.author, cancel_others=True, reset_timeout=True)
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
						nonlocal on_click

						date_=int(time.time())
						con=await helper.connect("db/video.db")
						cur=await helper.cursor(con)
						await cur.execute("INSERT INTO video VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", (ctx.author.id, str(title.content), str(description), str(attach.content), 0, 0, 0, f'["{ctx.author.id}"]', f'["{ctx.author.id}"]', "link", date_, token, f'["{ctx.author.id}"]', "n", nsfw.content, 0))
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
							color=self.embed_color
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
						nonlocal on_click

						await inter.reply(
							content="Declined!", 
							type=ResponseType.UpdateMessage,
							embed=discord.Embed(
								title=title.content,
								description=description if len(description) > 1 else "This video dont have a description",
								color=self.embed_color
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
	@commands.cooldown(1, 4, commands.BucketType.user)
	async def _videos(self, ctx):
		
		data=await helper.find_in_video(ctx.author.id, False, mode="all")
		channel_data=await helper.find_in_channel(ctx.author.id)
		info = await helper.find_in_info(ctx.author.id)
		
		if not channel_data:
			await ctx.send(embed=self.channel_error)
			return
		
		if info[2] == 'no':
			await ctx.send(embed=self.login_error)
			return

		video=int(channel_data[8]) 
		i = video - 1

		if not data or i < 0:
			await ctx.send(embed=self.video_error)
			return

		if video > 1 and len(data) > 1: 
			while True:
				raw_date=datetime.datetime.fromtimestamp(int(data[i][10]))
				date_time=raw_date.strftime("%m/%d/%Y")
				msg=await ctx.send(
					embed=discord.Embed(
						title='...' if not ctx.channel.is_nsfw() and data[i][14] == 'y' else data[i][1],
						url='' if not ctx.channel.is_nsfw() and data[i][14] == 'y' else data[i][3],
						description="This video is set to nsfw setting! Make sure to access this video in nsfw channels!" if not ctx.channel.is_nsfw() and data[i][14] == 'y' else data[i][2],
						color=discord.Color.red() if data[i][14] == 'y' else self.embed_color
						).set_footer(
							text=f"Videos {i + 1}/{video} | Date: {date_time} | ID: {data[i][11]}",
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
									custom_id="left-button"
								),
								Button(
									style=ButtonStyle.red,
									label="",
									emoji="<:tick_no:874284510575996968>",
									custom_id="delete-button",
								),
								Button(
									style=ButtonStyle.blurple,
									label="",
									emoji="🔢",
									custom_id="select-button",
								),
								Button(
									style=ButtonStyle.blurple,
									label="",
									emoji="\U000027a1",
									custom_id="right-button"
								)
							)
						]
					)
	
				file=await ctx.send(
					'Search this video in nsfw channel!' if data[i][14] == 'y' else data[i][3],
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
								style=ButtonStyle.grey,
								label=channel_data[4],
								emoji="<:user_icon:877535226694352946>",
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

				while True:
					try:
						inter = await ctx.wait_for_button_click(lambda inter: inter.author == ctx.author and inter.message.id == msg.id and inter.channel == ctx.channel, timeout=15)
						if inter.author != ctx.author:
							await inter.reply(embed=discord.Embed(
								description="You are not the member who use this command!",
								color=discord.Color.red()
							),
								ephemeral=True
							)
							
						else:
							break

					except asyncio.TimeoutError:
							await ctx.send(embed=discord.Embed(
								title="Timeout!",
								description="I have stop the command due to its long activity!",
								color=discord.Color.red()
							))
							return
					
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
							color=self.embed_color,
						)
					)
					break

				elif inter.clicked_button.custom_id == "select-button": #Select Button
					try:
						await inter.reply(
							ctx.author.mention, 
							embed=discord.Embed(
								description=f"What video you want to view? You have **{video}** videos",
								color=self.embed_color
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
			i = 0
			raw_date=datetime.datetime.fromtimestamp(int(data[i][10]))
			date_time=raw_date.strftime("%m/%d/%Y")
			msg=await ctx.send(
			embed=discord.Embed(
					title='...' if not ctx.channel.is_nsfw() and data[i][14] == 'y' else data[i][1],
					url='' if not ctx.channel.is_nsfw() and data[i][14] == 'y' else data[i][3],
					description="This video is set to nsfw setting! Make sure to access this video in nsfw channels!" if not ctx.channel.is_nsfw() and data[i][14] == 'y' else data[i][2],
					color=discord.Color.red() if data[i][14] == 'y' else self.embed_color
				).set_footer(
					text=f"Videos 1/1 | Date: {date_time} | ID: {data[i][11]}",
					icon_url=channel_data[3]
				).set_author(
					name=f"{ctx.author.name} (@{channel_data[1]})",
					icon_url=channel_data[3]
				)
			)
			file=await ctx.send(
				'Search this video in nsfw channel!' if data[i][14] == 'y' and not ctx.channel.is_nsfw() else data[i][3],
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
							style=ButtonStyle.grey,
							label=channel_data[4],
							emoji="<:user_icon:877535226694352946>",
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

	@commands.command("view", description="View a video with its ID")
	@commands.cooldown(1, 5, commands.BucketType.user)
	async def _view(self, ctx, *,video_ID):
		if not ctx.author.id in self.bot.owner_ids:
			await ctx.send("This command is under renovation. Comeback after 30 mins!")
			return
		
		loop=True
		con=await helper.connect('db/video.db')
		cur=await helper.cursor(con)

		await cur.execute("SELECT * FROM video WHERE ID = ?", (video_ID,)) 
		data=await cur.fetchone()

		if not data:
			await ctx.send(embed=discord.Embed(
				description="You put a wrong video ID!",
				color=discord.Color.red()
			))
			return
			
		if not data[13] == "n":
			await ctx.send(embed=discord.Embed(
				description="Oops! That video got disabled or got deleted by the owner!",
				color=discord.Color.red()
			))
			return

		user=await self.bot.fetch_user(data[0])
		await cur.close()
		await con.close()
		
		i = 0
		while True:
			con=await helper.connect('db/info.db')
			cur=await helper.cursor(con)
			info=await helper.find_in_info(ctx.author.id)
			viewed=ast.literal_eval(info[6])
			viewed.append(int(video_ID))
			await cur.execute("UPDATE info SET viewed = ? WHERE member_id = ?", (str(viewed), ctx.author.id))
			await con.commit()
			await cur.close()
			await con.close()

			data=await helper.view(video_ID)
			channel_data=await helper.find_in_channel(int(data[i][8]))
			con=await helper.connect("db/video.db")
			cur=await helper.cursor(con)

			con2=await helper.connect("db/channel.db")
			cur2=await helper.cursor(con2)
			
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
						title='...' if not ctx.channel.is_nsfw() and data[i][12] == 'y' else data[i][1],
						url='' if not ctx.channel.is_nsfw() and data[i][12] == 'y' else data[i][0],
						description="This video is set to nsfw setting! Make sure to access this video in nsfw channels!" if not ctx.channel.is_nsfw() and data[i][12] == 'y' else data[i][2],
						color=discord.Color.red() if data[i][12] == 'y' else self.embed_color
					).set_footer(
						text=f"Videos 1/{len(data)} | Date: {date_time} | ID: {data[i][10]}",
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
					'Search this video in nsfw channel!' if not ctx.channel.is_nsfw() and data[i][12] == 'y' else data[i][0],
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
								style=ButtonStyle.grey,
								label=channel_data[4],
								emoji="<:user_icon:877535226694352946>",
								custom_id="subs-button",
								disabled=True if str(ctx.author.id) in ast.literal_eval(channel_data[11]) else False
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
					try:
						inter = await ctx.wait_for_button_click(lambda inter: inter.message.id == msg.id or inter.message.id == file.id and inter.channel == ctx.channel, timeout=100)
						if inter.author != ctx.author:
							await inter.reply(embed=discord.Embed(
								description="You are not the member who use this command!",
								color=discord.Color.red()
							), 
								ephemeral=True
							)
							
						else:
							break

					except asyncio.TimeoutError:
						await msg.delete()
						await file.delete()
						await ctx.send(embed=discord.Embed(
							title="Timeout!",
							description="I have stop the command due to its long activity!",
							color=discord.Color.red()
						))
						return

				button_id = inter.clicked_button.custom_id
				
				if button_id == "subs-button":
					info_con=await helper.connect('db/info.db')
					info_cur=await helper.cursor(info_con)
					info=await info_cur.execute("SELECT subscribed FROM info WHERE member_id = ?", (ctx.author.id,))
					info=await info.fetchone()
					info_data=ast.literal_eval(info[0])
					info_data.append(data[i][10])
					await info_cur.execute("UPDATE info SET subscribed = ? WHERE member_id = ?", (str(info_data), ctx.author.id))
					await info_con.commit()
					await info_cur.close()
					await info_con.close()

					subs=ast.literal_eval(channel_data[11])
					if not str(ctx.author.id) in subs:
						subs.append(str(ctx.author.id))
						await inter.send(embed=discord.Embed(
							description=f"{ctx.author.mention} Sub the channel!",
							color=self.embed_color
						),
							ephemeral=True
						)
		
						await cur2.execute("UPDATE channel SET subscribers = subscribers + 1 WHERE member_id = ?", (channel_data[0],))
						await cur2.execute("UPDATE channel SET old_subs = ? WHERE member_id = ?", (str(subs), channel_data[0]))
						await con2.commit()
					
					await con2.commit()

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
									style=ButtonStyle.grey,
									label=channel_data[4] + 1,
									emoji="<:user_icon:877535226694352946>",
									custom_id="subs-button",
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
									disabled=True if str(ctx.author.id) in ast.literal_eval(data[i][7]) else False
								)
							)
						]
					)

					loop = False
					await cur2.close()
					await cur.close()
					await con2.close()
					await con.close()



				elif button_id == "delete-button": #Delete Button
					await msg.delete()
					await file.delete()
					await ctx.send(embed=discord.Embed(
							description=f"{ctx.author.mention} thanks for using Tango bot :blush:",
							color=self.embed_color,

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
						color=self.embed_color
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
									style=ButtonStyle.grey,
									label=channel_data[4],
									emoji="<:user_icon:877535226694352946>",
									custom_id="subs-button",
									disabled=True if str(ctx.author.id) in ast.literal_eval(channel_data[11]) else False
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
						color=self.embed_color
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
									style=ButtonStyle.grey,
									label=channel_data[4],
									emoji="<:user_icon:877535226694352946>",
									custom_id="subs-button",
									disabled=True if str(ctx.author.id) in ast.literal_eval(channel_data[11]) else False
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
				

			
	@commands.command("search", description="Search up videos that got posted by other members!")
	@commands.cooldown(1, 6, commands.BucketType.user)
	async def _search(self, ctx, *,name):
		loop=True
		if not ctx.author.id in self.bot.owner_ids:
			await ctx.send("This command is under renovation. Comeback after 30 mins!")
			return

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
				videos=await helper.find_videos(name)
				data=[x for x in videos]
				
				con=await helper.connect('db/info.db')
				cur=await helper.cursor(con)
				info=await helper.find_in_info(ctx.author.id)
				viewed=ast.literal_eval(info[6])
				viewed.append(data[i][10])
				await cur.execute("UPDATE info SET viewed = ? WHERE member_id = ?", (str(viewed), ctx.author.id))
				await con.commit()
				await cur.close()
				await con.close()

				channel_data=await helper.find_in_channel(data[i][8])
				con=await helper.connect("db/video.db")
				cur=await helper.cursor(con)
				con2=await helper.connect("db/channel.db")
				cur2=await helper.cursor(con2)

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
						user=await self.bot.fetch_user(channel_data[0])
						msg=await ctx.send(
						embed=discord.Embed(
							title='...' if not ctx.channel.is_nsfw() and data[i][12] == 'y' else data[i][1],
							url='' if not ctx.channel.is_nsfw() and data[i][12] == 'y' else data[i][0],
							description="This video is set to nsfw setting! Make sure to access this video in nsfw channels!" if not ctx.channel.is_nsfw() and data[i][12] == 'y' else data[i][2],
							color=discord.Color.red() if data[i][12] == 'y' else self.embed_color
						).set_footer(
							text=f"Videos {i + 1}/{len(data)} | Date: {date_time} | ID: {data[i][10]}",
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
										custom_id="delete-button",
										disabled=False
									),
									Button(
										style=ButtonStyle.blurple,
										label="",
										emoji="\U000027a1",
										custom_id="right-button"
									)
								)
							]
						) 
						file=await ctx.send(
							'Search this video in nsfw channel!' if not ctx.channel.is_nsfw() and data[i][12] == 'y' else data[i][0],
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
										style=ButtonStyle.grey,
										label=channel_data[4],
										emoji="<:user_icon:877535226694352946>",
										custom_id="subs-button",
										disabled=True if str(ctx.author.id) in ast.literal_eval(channel_data[11]) else False
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

					while True:
						try:
							inter = await ctx.wait_for_button_click(lambda inter: inter.message.id == msg.id or inter.message.id == file.id and inter.channel == ctx.channel, timeout=100)	
							
							if inter.author != ctx.author:
								await inter.reply(embed=discord.Embed(
									description="You are not the member who use this command!",
									color=discord.Color.red()
								), 
									ephemeral=True
								)
								
							else:
								break

						except asyncio.TimeoutError:
							await msg.delete()
							await file.delete()
							await ctx.send(embed=discord.Embed(
								title="Timeout!",
								description="I have stop the command due to its long activity!",
								color=discord.Color.red()
							))
							return

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
	
						await cur.close()
						await cur2.close()
						await con.close()
						await con2.close()

					elif button_id == "delete-button": #Delete Button
						await msg.delete()
						await file.delete()
						await ctx.send(embed=discord.Embed(
								description=f"{ctx.author.mention} thanks for using Tango bot :blush:",
								color=self.embed_color,
							)
						)
						
						await cur.close()
						await cur2.close()
						await con.close()
						await con2.close()
						break

					elif button_id == "subs-button":
						info_con=await helper.connect('db/info.db')
						info_cur=await helper.cursor(info_con)
						info=await info_cur.execute("SELECT subscribed FROM info WHERE member_id = ?", (ctx.author.id,))
						info=await info.fetchone()
						info_data=ast.literal_eval(info[0])
						info_data.append(data[i][10])
						await info_cur.execute("UPDATE info SET subscribed = ? WHERE member_id = ?", (str(info_data), ctx.author.id))
						await info_con.commit()
						await info_cur.close()
						await info_con.close()
						


						subs=ast.literal_eval(channel_data[11])
						if not str(ctx.author.id) in subs:
							subs.append(str(ctx.author.id))
		
							await inter.send(embed=discord.Embed(
								description=f"{ctx.author.mention} Sub the channel!",
								color=self.embed_color
							),
								ephemeral=True
							)
			
							await cur2.execute("UPDATE channel SET subscribers = subscribers + 1 WHERE member_id = ?", (channel_data[0],))
							await cur2.execute("UPDATE channel SET old_subs = ? WHERE member_id = ?", (str(subs), channel_data[0]))
							await con2.commit()

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
										style=ButtonStyle.grey,
										label=channel_data[4] + 1,
										emoji="<:user_icon:877535226694352946>",
										custom_id="subs-button",
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

						loop = False
						await cur.close()
						await cur2.close()
						await con.close()
						await con2.close()

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
							color=self.embed_color
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
										style=ButtonStyle.grey,
										label=channel_data[4],
										emoji="<:user_icon:877535226694352946>",
										custom_id="subs-button",
										disabled=True if str(ctx.author.id) in ast.literal_eval(channel_data[11]) else False
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
							color=self.embed_color
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
										style=ButtonStyle.grey,
										label=channel_data[4],
										emoji="<:user_icon:877535226694352946>",
										custom_id="subs-button",
										disabled=True if str(ctx.author.id) in ast.literal_eval(channel_data[11]) else False
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
				videos=await helper.find_videos(name)
				data=[x for x in videos]

				con=await helper.connect('db/info.db')
				cur=await helper.cursor(con)
				info=await helper.find_in_info(ctx.author.id)
				viewed=ast.literal_eval(info[6])
				viewed.append(data[i][10])
				await cur.execute("UPDATE info SET viewed = ? WHERE member_id = ?", (str(viewed), ctx.author.id))
				await con.commit()
				await cur.close()
				await con.close()

				channel_data=await helper.find_in_channel(data[i][8])
				con=await helper.connect("db/video.db")
				cur=await helper.cursor(con)
				user=await self.bot.fetch_user(channel_data[0])
				con2=await helper.connect("db/channel.db")
				cur2=await helper.cursor(con2)

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
							title='...' if not ctx.channel.is_nsfw() and data[i][12] == 'y' else data[i][1],
							url='' if not ctx.channel.is_nsfw() and data[i][12] == 'y' else data[i][0],
							description="This video is set to nsfw setting! Make sure to access this video in nsfw channels!" if not ctx.channel.is_nsfw() and data[i][12] == 'y' else data[i][2],
							color=discord.Color.red() if data[i][12] == 'y' else self.embed_color
						).set_footer(
							text=f"Videos 1/{len(data)} | Date: {date_time} | ID: {data[i][10]}",
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
						'Search this video in nsfw channel!' if not ctx.channel.is_nsfw() and data[i][12] == 'y' else data[i][0],
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
									style=ButtonStyle.grey,
									label=channel_data[4],
									emoji="<:user_icon:877535226694352946>",
									custom_id="subs-button",
									disabled=True if str(ctx.author.id) in ast.literal_eval(channel_data[11]) else False
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
						inter = await ctx.wait_for_button_click(lambda inter: inter.message.id == msg.id or inter.message.id == file.id and inter.channel == ctx.channel, timeout=100)
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
					
					if button_id == "subs-button":
						info_con=await helper.connect('db/info.db')
						info_cur=await helper.cursor(info_con)
						info=await info_cur.execute("SELECT subscribed FROM info WHERE member_id = ?", (ctx.author.id,))
						info=await info.fetchone()
						info_data=ast.literal_eval(info[0])
						info_data.append(data[i][10])
						await info_cur.execute("UPDATE info SET subscribed = ? WHERE member_id = ?", (str(info_data), ctx.author.id))
						await info_con.commit()
						await info_cur.close()
						await info_con.close()
						
					

						subs=ast.literal_eval(channel_data[11])
						if not str(ctx.author.id) in subs:
							subs.append(str(ctx.author.id))
		
							await inter.send(embed=discord.Embed(
								description=f"{ctx.author.mention} Sub the channel!",
								color=self.embed_color
							),
								ephemeral=True
							)
			
							await cur2.execute("UPDATE channel SET subscribers = subscribers + 1 WHERE member_id = ?", (channel_data[0],))
							await cur2.execute("UPDATE channel SET old_subs = ? WHERE member_id = ?", (str(subs), channel_data[0]))
							await con2.commit()
						
						await con2.commit()
						await cur2.close()
						await con2.close()

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
										style=ButtonStyle.grey,
										label=channel_data[4] + 1,
										emoji="<:user_icon:877535226694352946>",
										custom_id="subs-button",
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
										disabled=True if str(ctx.author.id) in ast.literal_eval(data[i][7]) else False
									)
								)
							]
						)

						loop = False
						await cur2.close()
						await cur.close()
						await con2.close()
						await con.close()

					elif button_id == "delete-button": #Delete Button
						await msg.delete()
						await file.delete()
						await ctx.send(embed=discord.Embed(
								description=f"{ctx.author.mention} thanks for using Tango bot :blush:",
								color=self.embed_color,

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
							color=self.embed_color
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
										style=ButtonStyle.grey,
										label=channel_data[4],
										emoji="<:user_icon:877535226694352946>",
										custom_id="subs-button",
										disabled=True if str(ctx.author.id) in ast.literal_eval(channel_data[11]) else False
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
							color=self.embed_color
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
										style=ButtonStyle.grey,
										label=channel_data[4],
										emoji="<:user_icon:877535226694352946>",
										custom_id="subs-button",
										disabled=True if str(ctx.author.id) in ast.literal_eval(channel_data[11]) else False
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
					if isinstance(e, asyncio.TimeoutError):
						await msg.delete()
						await file.delete()
						await ctx.send(embed=discord.Embed(
							title="Timeout!",
							description="I have stop the command due to its long activity!",
							color=discord.Color.red()
						))
						return
		else:
			msg=await ctx.send(embed=discord.Embed(
				title=f"Searched for '{name}'",
				color=self.embed_color
			).set_footer(
				text=f"Found 0 result! Try again with diffreant quary"
			)
		)
	
	@commands.command("setting", description="Setting up your channel and profile info", aliases=['set'])
	@commands.cooldown(1, 4, commands.BucketType.user)
	async def _setting(self, ctx):


		db=await helper.connect("db/channel.db")
		db2=await helper.connect("db/info.db")
		cur=await helper.cursor(db)
		info=await helper.cursor(db2)
		info_data=await helper.find_in_info(ctx.author.id)
		user=await helper.find_user(ctx.author.id)

		if not user:
			await ctx.send(embed=self.channel_error)
			return

		if info_data[2] == 'no':
			await ctx.send(embed=self.login_error)
			return

		embed=await ctx.send(embed=discord.Embed(
			title="<a:moving_gear:874897860469088296> Setting Menu",
			description="Is there anything i could help?",
			color=self.embed_color
		).set_footer(
			text="Select what you need to change through the dropdown below this embed | Considering voting Tango in DBL with p!vote command!"
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
				try:
					inter = await embed.wait_for_dropdown(check=lambda inter: inter.author == ctx.author, timeout=10)
					if inter.author != ctx.author:
						await inter.reply(embed=discord.Embed(
							description="You are not the member who use this command!",
							color=discord.Color.red()
						), 
							ephemeral=True
						)
						
					else:
						break

				except asyncio.TimeoutError:
					await ctx.send(embed=discord.Embed(
						title="Timeout",
						description="I have stop the command due to its long activity!",
						color=discord.Color.red()
					))
					return

			label = "".join([option.label for option in inter.select_menu.selected_options])
			value= "".join([option.value for option in inter.select_menu.selected_options])
			if value == "channel":
				await inter.reply(embed=discord.Embed(
					title="Type your change",
					description=f"Type your new {label}! Must not have special characters and Must be minimum of 5 to 13 characters",
					color=self.embed_color
				).set_footer(
					text="You have 120 seconds to do this"
				))
				msg=await self.bot.wait_for("message", check=lambda x: x.author == ctx.author and x.channel == ctx.channel, timeout=120)
				await cur.execute("UPDATE channel SET channel = ? WHERE member_id = ?", (msg.content, ctx.author.id))
				await ctx.send(embed=discord.Embed(
						description="Done! Check it using t!profile",
						color=self.embed_color
					)
				)
				await db.commit()
				await cur.close()

			elif value == "description":
				await inter.reply(embed=discord.Embed(
					title="Type your change",
					description=f"Type your new {label}!",
					color=self.embed_color
				).set_footer(
					text="You have 120 seconds to do this"
				))
				msg=await self.bot.wait_for("message", check=lambda x: x.author == ctx.author and x.channel == ctx.channel, timeout=120)
				await cur.execute("UPDATE channel SET description = ? WHERE member_id = ?", (msg.content, ctx.author.id))
				await ctx.send(embed=discord.Embed(
						description="Done! Check it using t!profile",
						color=self.embed_color
					)
				)
				
				await db.commit()
				await cur.close()

			elif value == "banner":
				await inter.reply(embed=discord.Embed(
					title="Type your change",
					description=f"Type your new {label}!\nThe link must be an https link, mp4, mp3, gif, png, jpg, or webt!",
					color=self.embed_color
				).set_footer(
					text="You have 120 seconds to do this"
				))
				msg=await self.bot.wait_for("message", check=lambda x: x.author == ctx.author and x.channel == ctx.channel, timeout=120)
				
				if msg.attachments or msg.content.startswith("http"):
					if msg.attachments:
						for x in msg.attachments:
							await cur.execute("UPDATE channel SET banner = ? WHERE member_id = ?", (str(x), ctx.author.id))
							await ctx.send(embed=discord.Embed(
									description="Done! Check it using t!profile",
									color=self.embed_color
								)
							)
							break
						
					else:
						await cur.execute("UPDATE channel SET banner = ? WHERE member_id = ?", (msg.content, ctx.author.id))
						await ctx.send(embed=discord.Embed(
								description="Done! Check it using t!profile",
								color=self.embed_color
							)
						)
						
				await db.commit()
				await cur.close()
			
	#=================================================

			elif value == "gender":
				Message=await inter.reply(embed=discord.Embed(
					title="Select your change",
					description="Select your new Gender!",
					color=self.embed_color
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
			
				try:
					gender = await Message.wait_for_dropdown(check=lambda inter: inter.author == ctx.author, timeout=10)
				except asyncio.TimeoutError:
					await ctx.send(embed=discord.Embed(
						title="Timeout",
						description="I have stop the command due to its long activity!",
						color=discord.Color.red()
					))
					return

				label = "".join([option.label for option in gender.select_menu.selected_options])
				await gender.reply(embed=discord.Embed(
						description="Done! Check it using p!profile",
						color=self.embed_color
					)
				)
			
				await info.execute("UPDATE info SET gender = ? WHERE member_id = ?", (label, ctx.author.id))
				
				await db2.commit()
				await info.close()

			elif value == "email":
				await inter.reply(embed=discord.Embed(
					title="Type your change",
					description=f"Type your new email! (e.g EpicUser123, EpicDiscord123)\nMust not have special characters and Must be minimum of 5 to 13 characters",
					color=self.embed_color
				).set_footer(
					text="You have 120 seconds to do this"
				))
				msg=await self.bot.wait_for("message", check=lambda x: x.author == ctx.author and x.channel == ctx.channel, timeout=120)

				for x in self.special_characters:
					if x in msg.content:
						await ctx.send(embed=discord.Embed(
							description="Dont put special characters in email!",
							color=discord.Color.red()
						))
						return 

	
				await info.execute("UPDATE info SET email = ? WHERE member_id = ?", (msg.content, ctx.author.id))
				await ctx.send(embed=discord.Embed(
						description="Done! Check it using t!profile",
						color=self.embed_color
					)
				)

				await db2.commit()
				await info.close()

			elif value == "password":
				await inter.reply(f"{ctx.author.mention} check your DM")
				await ctx.author.send(embed=discord.Embed(
					title="Type your change",
					description=f"Type your new Password! Must not have special characters and Must be minimum of 5 to 13 characters",
					color=self.embed_color
				).set_footer(
					text="You have 120 seconds to do this"
				))
				msg=await self.bot.wait_for("message", check=lambda x: x.author == ctx.author and isinstance(x.channel, discord.DMChannel), timeout=120)
				
				for x in self.special_characters:
					if x in msg.content:
						await ctx.author.send(embed=discord.Embed(
							description="Dont put special characters in password!",
							color=discord.Color.red()
						))
						return 

				await ctx.author.send(f"Your password are ||{msg.content}||")
				await info.execute("UPDATE info SET password = ? WHERE member_id = ?", (msg.content, ctx.author.id))
				await ctx.send(ctx.author.mention, embed=discord.Embed(
						description="Done! Check it using p!profile",
						color=self.embed_color
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


	@commands.command("login", description="Use for login to your account by entering the account email and password!")
	@commands.cooldown(1, 5, commands.BucketType.user)
	async def _login(self, ctx):

		data=await helper.find_in_info(ctx.author.id)
		channel=await helper.find_in_channel(ctx.author.id)

		con=await helper.connect("db/info.db")
		cur=await helper.cursor(con)
		
		if not data or not channel:
			await ctx.send("Oops you are not in the database! To be able to login to existing accounts you need to make your own account first using `p!start` command then use `p!login` again!")
			return

		buttons = ActionRow(
			Button(
				style=ButtonStyle.green,
				label="Continue",
				emoji="<:tick_yes:874284510135607350>",
				custom_id="green"
			),
			Button(
				style=ButtonStyle.red,
				label="Abort",
				emoji="<:tick_no:874284510575996968>",
				custom_id="red"
			)
		)

		if data[2] == 'no' or not data:
			msg=await ctx.send(embed=discord.Embed(
				title="Login!",
				description="Hey there, you are one step closer to login into your account! if you want to cancel this command you can always type `abort`. Please press the green button to continue or red button to cancel this command. Once you press the green button the bot will guide you through the rest",
				color=self.embed_color
			), components=[
				buttons
			])

			on_click=msg.create_click_listener(timeout=120)

			@on_click.not_from_user(ctx.author, cancel_others=True, reset_timeout=True)
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
				nonlocal data
				nonlocal channel
				nonlocal on_click
				
				await inter.reply(
					type=7,
					embed=discord.Embed(
					title="Step 1",
					description="Enter the email name that you type in `p!start` command, It must be your email not others!",
					color=self.embed_color
				).add_field(
					name="Requirements!",
					value="\> Type your email name without any special characters! Except Underscore(_)\n\> Minimum of 5 to 15 characters!\n\> Make sure the spelling are correct!\n\> You may not use '@email' or similar word in this process!"
				).add_field(
					name="Example!",
					value="\> EpicUser123\n\> DiscordUser321",
					inline=True
				).set_footer(
					text=f"{ctx.author} • You can type abort to cancel this command!",
					icon_url=ctx.author.avatar_url
				), components=[

				])	
				try:
					email=await self.bot.wait_for("message", check=lambda msg: msg.author == ctx.author and msg.channel == ctx.channel, timeout=120.0)
				except asyncio.TimeoutError:
					await ctx.send(embed=discord.Embed(
						title="Timeout",
						description="I have stop the command due to its long activity!",
						color=discord.Color.red()
					))
					on_click.kill()

				raw_email=f"{email.content}@email.com"

				if email.content.lower() == "abort":
					await inter.edit(
						type=7,
						embed=discord.Embed(
							description="Aborting...",
							color=discord.Color.red()
				))	
					on_click.kill()
					return

				for x in self.special_characters:
					if x in email.content:
						await ctx.send(embed=discord.Embed(
							description="Dont put special characters in email name!",
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
				
				await cur.execute("SELECT * FROM info WHERE email = ?", (raw_email,))
				data=await cur.fetchone()
				if not data:
					await ctx.send(embed=discord.Embed(
						description=f"I cant find that email. Try another one!",
						color=discord.Color.red()
					))
					on_click.kill()
					return
				
				if data[2] == "yes":
					await ctx.send(embed=discord.Embed(
						description="Someone already logged into that account! Perhaps you put wrong email?",
						color=discord.Color.red()
					))
					on_click.kill()
					return
				
				
				await ctx.send(f"{ctx.author.mention} Check your DM!")
				#Password
				await ctx.author.send(
					embed=discord.Embed(
					title="Step 2",
					description=f"Type the password for an account with `{raw_email}` as its email",
					color=self.embed_color
				).add_field(
					name="Requirements!",
					value="\> Type your password without any special characters! Except Underscore(_)\n\> Minimum of 5 to 15 characters!\n"
				).set_footer(
					text=f"{ctx.author} • You can type abort to cancel this command!",
					icon_url=ctx.author.avatar_url
				), components=[

				])
				password=await self.bot.wait_for("message", check=lambda x: x.author == ctx.author and isinstance(x.channel, discord.DMChannel))

				if password.content.lower() == "abort":
					await ctx.author.send(
						type=7,
						embed=discord.Embed(
							description="Aborting...",
							color=discord.Color.red()
					))	
					on_click.kill()
					return
				
				for x in self.special_characters:
					if x in password.content:
						await ctx.author.send(embed=discord.Embed(
							description="Dont put special characters in password name!",
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

				pass_=data[4]
				e=base64.b64decode(pass_).decode()
				if e != password.content:
					await ctx.author.send(embed=discord.Embed(
						description=f"Wrong password, pls check if the password is correct!",
						color=discord.Color.red()
					))
					on_click.kill()
					return

				await ctx.author.send(f"Back to {ctx.channel.mention}")


				msg=await ctx.send(
					content="Is this you? Click the green button if this is you, Click the red one if it isn't",
					embed=discord.Embed(
						title="Profile Menu!",
						description=channel[2],
						color=self.embed_color,
						timestamp=ctx.message.created_at
						).set_author(
							name=f"{ctx.author.name} (@{channel[1]})",
							icon_url=channel[3]
						).set_footer(
							text=f"Source: @{channel[1]} | ID: {ctx.author.id}",
							icon_url=channel[3]
						).add_field(
							name="<:follow:875659362264309791> Subs",
							value=channel[4]
						).add_field(
							name="<:blurple_camera:875659362331394058> Videos",
							value=channel[8]
						).add_field(
							name="🫂 Views",
							value=channel[7]
						).add_field(
							name="<:likes:875659362343993404> Likes",
							value=channel[5]
						).add_field(
							name="<:dislikes:875659362264309821> Dislikes",
							value=channel[6]
						).add_field(
							name="\u200b",
							value="\u200b"
						).add_field(
							name="Account Information",
							value="Here is all of your account information! You can change it using p!settingting command!",
							inline=False
						).add_field(
							name="🫂 Gender",
							value=data[1]
						).add_field(
							name="📧 email",
							value=data[3]
						).add_field(
							name="🔑 Password",
							value="||[Password Redacted]||",
							inline=False
						).add_field(
							name="⌛ Account Age",
							value=data[5]
				), components=[
						ActionRow(
							Button(
								style=ButtonStyle.green,
								label="Continue",
								emoji="<:tick_yes:874284510135607350>",
								custom_id="green"
							),
							Button(
								style=ButtonStyle.red,
								label="Abort",
								emoji="<:tick_no:874284510575996968>",
								custom_id="red"
							)
						)
					]
				)

				on_click.kill()
				on_click=msg.create_click_listener(timeout=60.0)

				@on_click.not_from_user(ctx.author, cancel_others=True, reset_timeout=True)
				async def on_wrong_user(inter):
					await inter.reply(
						embed=discord.Embed(
						description="You are not the member who use this command!",
						color=discord.Color.red()
					), 
						ephemeral=True
					)
	
				@on_click.matching_id("red")
				async def _Red(inter):
					await inter.reply(
						type=7,
						content="Aborting...",
						embed=discord.Embed(
						description="Aborting...",
						color=discord.Color.red()
					), components=[

					])

					on_click.kill()
					return

				@on_click.matching_id("green")
				async def _Green(inter):
					nonlocal on_click
					nonlocal con
					nonlocal cur

					y='yes'
					if data[0] == ctx.author.id:
						await cur.execute("UPDATE info SET verified = ? WHERE email = ?", (y, raw_email))
						await con.commit()
						await cur.close()
						await con.close()

						await inter.reply(
							type=7,
							content=f"You successfully logged in as `{channel[1]}`. Now you can use all Social commands! use `p!help social` for all info about social ",
							embed=discord.Embed(
								title="Profile Menu!",
								description=channel[2],
								color=self.embed_color,
								timestamp=ctx.message.created_at
								).set_author(
									name=f"{ctx.author.name} (@{channel[1]})",
									icon_url=channel[3]
								).set_footer(
									text=f"Source: @{channel[1]} | ID: {ctx.author.id}",
									icon_url=channel[3]
								).add_field(
									name="<:follow:875659362264309791> Subs",
									value=channel[4]
								).add_field(
									name="<:blurple_camera:875659362331394058> Videos",
									value=channel[8]
								).add_field(
									name="🫂 Views",
									value=channel[7]
								).add_field(
									name="<:likes:875659362343993404> Likes",
									value=channel[5]
								).add_field(
									name="<:dislikes:875659362264309821> Dislikes",
									value=channel[6]
								).add_field(
									name="\u200b",
									value="\u200b"
								).add_field(
									name="Account Information",
									value="Here is all of your account information! You can change it using p!settingting command!",
									inline=False
								).add_field(
									name="🫂 Gender",
									value=data[1]
								).add_field(
									name="📧 email",
									value=data[3]
								).add_field(
									name="🔑 Password",
									value="||[Password Redacted]||",
									inline=False
								).add_field(
									name="⌛ Account Age",
									value=data[5]
								)
							)

						on_click.kill()
						return
					else:
						await ctx.send("For now you can only access to an account that you create with `p!start` command! This will be fix later!")
						# con=await helper.connect("db/info.db")
						# cur=await helper.cursor(con)

						# await cur.execute("SELECT * FROM info WHERE member_id = ?", (data[0],))
						# user_info=await cur.fetchone()

						# await cur.execute("SELECT * FROM info WHERE member_id = ?", (ctx.author.id,))
						# author_info=await cur.fetchone()






				

			@on_click.matching_id("red")
			async def _red(inter):
				await inter.reply(
					type=7,
					embed=discord.Embed(
					description="Aborting...",
					color=discord.Color.red()
				), components=[

				])

				on_click.kill()

		else:
			await ctx.send(embed=discord.Embed(
				description=f"You already login to your account as `{channel[1]}` If thats not you use `p!logout` command and use the login command again!",
				color=discord.Color.red()
			))


	@commands.command("logout", description="Logout from an account!")
	@commands.cooldown(1, 5, commands.BucketType.user)
	async def _logout(self, ctx):

		data=await helper.find_in_channel(ctx.author.id)
		info=await helper.find_in_info(ctx.author.id)
		
		if not data or not info:
			await ctx.send(embed=self.channel_error)
			return

		if info[2] == 'no':
			await ctx.send(embed=discord.Embed(
				description="You already logout from your account! Please use `p!login` command to login to your account!",
				color=discord.Color.red()
			))
			return

		msg=await ctx.send(
			"**Confirmation**\nAre sure you want to logout from this account?",
			embed=discord.Embed(
				title="Profile Menu!",
				description=data[2],
				color=self.embed_color,
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
					value="Here is all of your account information! You can change it using p!setting command!",
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
				), components=[
					ActionRow(
						Button(
							style=ButtonStyle.green,
							label="Continue",
							emoji="<:tick_yes:874284510135607350>",
							custom_id="green"
						),
						Button(
							style=ButtonStyle.red,
							label="Abort",
							emoji="<:tick_no:874284510575996968>",
							custom_id="red"
						)
					)
				]
			)

		on_click=msg.create_click_listener(timeout=20)

		@on_click.not_from_user(ctx.author, cancel_others=True, reset_timeout=False)
		async def _not_from_author(inter):
			await inter.reply(
				embed=discord.Embed(
					description="You are not the member who use this command!",
					color=discord.Color.red()
				), 
					ephemeral=True
				)

		@on_click.matching_id("green")
		async def _Green_(inter):
			nonlocal on_click
			con=await helper.connect("db/info.db")
			cur=await helper.cursor(con)
			await cur.execute("UPDATE info SET verified = ? WHERE member_id = ?", ('no', ctx.author.id))
			
			await con.commit()
			await cur.close()
			await con.close()
			
			await inter.reply(
				type=7,
				content=" ",
				embed=discord.Embed(
					description="You have succesfuly logout from your account! Please use `p!login` command to get access to your account!",
					color=discord.Color.red()
				), components=[

				]
			)
			on_click.kill()
			return

		@on_click.matching_id("red")
		async def red_(inter):
			nonlocal on_click
			await inter.reply(
				type=7,
				content="aborting...",
				embed=discord.Embed(
					description="Aborting...",
					color=discord.Color.red()
				), components=[

				]
			)
			on_click.kill()
			return

	@commands.command("comment", description="Comment a video! make sure to only provide the video id if you want to view all comments if not then provide the comment msg to comment a video!")
	@commands.cooldown(1, 3, commands.BucketType.user)
	async def _comment(self, ctx, video_id, *,msg=None):
		try:
			video_id=int(video_id)
		except ValueError:
			await ctx.send(embed=discord.embed(
				description="Video ID must contain numbers!",
				color=discord.Color.red()
			))
		
		video=await helper.is_video(video_id)
		data=await helper.find_in_channel(ctx.author.id)
		info=await helper.find_in_info(ctx.author.id)
		
		if not video:
			await ctx.send(embed=discord.Embed(
				description="You put a wrong video ID!",
				color=discord.Color.red()
			))
			return

		if not data or not info:
			await ctx.send(embed=self.channel_error)
			return

		if info[2] == 'no':
			await ctx.send(embed=self.login_error)
			return

		if msg:
			if len(msg) > 300:
				await ctx.send(
					embed=discord.Embed(
						description="Your comment is too long! Maximum character is between 1 to 300 characters",
						color=discord.Color.red()
					)
				)
				return

			await helper.comments(self.bot, ctx.author.id, video_id, msg)
			await ctx.send("Posted your comment!")
			
			con=await helper.connect("db/video.db")
			cur=await helper.cursor(con)
			await cur.execute("UPDATE video SET comments = comments + 1 WHERE ID = ?", (video_id,))

			await con.commit()
			await cur.close()
			await con.close()
		
		else:
			
			con=await helper.connect("db/comment.db")
			cur=await helper.cursor(con)
			
			await cur.execute("SELECT commenter_id, content, comment_id, date FROM comments WHERE video_id = ?", (video_id,))
			data=await cur.fetchall()
 
			await cur.close()
			await con.close()
			
			con=await helper.connect("db/video.db")
			cur=await helper.cursor(con)
			await cur.execute("SELECT * FROM video WHERE ID = ?", (video_id,))
			video=await cur.fetchall()
 
			await cur.close()
			await con.close()

			tz=datetime.datetime.utcfromtimestamp(int(video[0][10]))
			con=await helper.connect("db/channel.db")
			cur=await helper.cursor(con)
			
			if not video:
				await ctx.send(embed=discord.Embed(
					description="This video doesnt have comments",
					color=discord.Color.red()
				))
				return
			
			if not ctx.channel.is_nsfw() and video[0][14] == "y":
				await ctx.send(embed=discord.Embed(
					description="This video is set to nsfw setting! Make sure to access this video in nsfw channels!",
					color=discord.Color.red()
				))
				return

			loop=True
			embed=None
			page = 0
			comments=len(data)
			if comments > 1:
				while True:
					commenter=await helper.find_in_channel(data[page][0])
					user=await self.bot.fetch_user(data[page][0])
					if loop == True:
						em=discord.Embed(
							title=f"Comments on '{video[0][1]}'",
							description=f"**[<t:{data[page][3]}:R> {user.name}]:** {data[page][1]}\n",
							color=self.embed_color,
							timestamp=tz
						).set_footer(
							text=f"Comments {page + 1}/{comments} | Comment ID: {data[page][2]} | Video ID: {video_id}",
							icon_url=commenter[3]
						).set_author(
							name=f"Commented by @{user.name}",
							icon_url=commenter[3]
						)

						embed=await ctx.send(
							embed=em,
							components=[
								ActionRow(
									Button(
										style=ButtonStyle.green,
										label="Scrollup",
										emoji="⏫",
										custom_id="up"
									),
									Button(
										style=ButtonStyle.red,
										emoji="<:tick_no:874284510575996968>",
										custom_id="delete-button"
									)
								),
								ActionRow(
									Button(
										style=ButtonStyle.green,
										label="Scrolldown",
										emoji="⏬",
										custom_id="down"
									)
								)
							]
						)

					else:
						em=discord.Embed(
							title=f"Comments on '{video[0][1]}'",
							description=f"**[<t:{data[page][3]}:R> {user.name}]:** {data[page][1]}\n",
							color=self.embed_color,
							timestamp=tz
						).set_footer(
							text=f"Comments {page + 1}/{comments} | Comment ID: {data[page][2]} | Video ID: {video_id}",
							icon_url=commenter[3]
						).set_author(
							name=f"Commented by @{user.name}",
							icon_url=commenter[3]
						)
						
						await embed.delete()
						embed=await ctx.send(
							embed=em,
							components=[
								ActionRow(
									Button(
										style=ButtonStyle.green,
										label="Scrollup",
										emoji="⏫",
										custom_id="up"
									),
									Button(
										style=ButtonStyle.red,
										emoji="<:tick_no:874284510575996968>",
										custom_id="delete-button"
									)
								),
								ActionRow(
									Button(
										style=ButtonStyle.green,
										label="Scrolldown",
										emoji="⏬",
										custom_id="down"
									)
								)
							]
						)

					while True:
						try:
							inter = await ctx.wait_for_button_click(lambda inter: inter.message == embed and inter.channel == ctx.channel, timeout=15.0)
						
							if inter.author != ctx.author:
								await inter.reply(embed=discord.Embed(
									description="You are not the member who use this command!",
									color=discord.Color.red()
								), 
									ephemeral=True
								)
								
							else:
								break

						except asyncio.TimeoutError:
							await ctx.send(embed=discord.Embed(
								title="Timeout!",
								description="I have stop the command due to its long activity!",
								color=discord.Color.red()
							))
							return

					button_id = inter.clicked_button.custom_id
					if button_id == "up":
						if page == (comments - 1):
							page = 0
							loop=False
						
						else:
							page += 1
							loop = False

					elif button_id == "down":
						if page == 0:
							page = (comments - 1)
							loop=False
						
						else:
							page -= 1
							loop = False

					elif button_id == "delete-button":
						await embed.delete()
						await ctx.send(
							embed=discord.Embed(
							description=f"{ctx.author.mention} thanks for using Tango bot :blush:",
							color=self.embed_color,
						)
					)
						break
			else:
				try:
					commenter=await helper.find_in_channel(data[page][0])
				except IndexError:
					await ctx.send(embed=discord.Embed(
						description="This video doesn't have comments! be the first one who did! use `p!comment <video id> <message>` to comment the video! and use `p!comment <video id>` to look the comments list!",
						color=discord.Color.red()
					))
					return

				user=await self.bot.fetch_user(data[page][0])
				em=discord.Embed(
					title=f"Comments on '{video[0][1]}'",
					description=f"**[<t:{data[page][3]}:R> {user.name}]:** {data[page][1]}\n",
					color=self.embed_color,
					timestamp=tz
				).set_footer(
					text=f"Comments {page + 1}/{comments} | Comment ID: {data[page][2]} | Video ID: {video_id}",
					icon_url=commenter[3]
				).set_author(
					name=f"Commented by @{user.name}",
					icon_url=commenter[3]
				)

				embed=await ctx.send(
					embed=em,
					components=[
						ActionRow(
							Button(
								style=ButtonStyle.green,
								label="Scrollup",
								emoji="⏫",
								disabled=True,
								custom_id="up"
							)
						),
						ActionRow(
							Button(
								style=ButtonStyle.green,
								label="Scrolldown",
								emoji="⏬",
								disabled=True,
								custom_id="down"
							)
						)
					]
				)

	@commands.command("delete", description="Delete a video through its ID")
	@commands.cooldown(1, 5, commands.BucketType.user)
	async def _delete(self, ctx, ID):
		channel_data=await helper.find_in_channel(ctx.author.id)
		info=await helper.find_in_info(ctx.author.id)
		con=await helper.connect("db/video.db")
		cur=await helper.cursor(con)

		await cur.execute("SELECT * FROM video WHERE ID = ?", (ID,))
		data=await cur.fetchone()
		
		if not channel_data:
			await ctx.send(embed=self.channel_error)
			return

		if info[2] == 'no':
			await ctx.send(embed=self.login_error)
			return

		if not data:
			await ctx.send(embed=discord.Embed(
				description="You put a wrong video ID!",
				color=discord.Color.red()
			))
			return
		
		if data[0] != ctx.author.id:
			await ctx.send(embed=discord.Embed(
				description="You're not the owner who uploaded this video!",
				color=discord.Color.red()
			)) 
			return

		if data[13] == 'y':
			await ctx.send(embed=discord.Embed(
				description="That video is already deleted!",
				color=discord.Color.red()
			))
			return

		
		
		raw_date=datetime.datetime.fromtimestamp(data[10])
		date_time=raw_date.strftime("%m/%d/%Y")
		msg=await ctx.send(
			"Are you sure you want to deleted this video?",
			embed=discord.Embed(
				title='...' if not ctx.channel.is_nsfw() and data[14] == 'y' else data[1],
				url='' if not ctx.channel.is_nsfw() and data[14] == 'y' else data[3],
				description="This video is set to nsfw setting! Make sure to access this video in nsfw channels!" if not ctx.channel.is_nsfw() and data[14] == 'y' else data[2],
				color=discord.Color.red() if data[14] == 'y' else self.embed_color
			).set_footer(
				text=f"Videos 1/1 | Date: {date_time} | ID: {data[11]}",
				icon_url=channel_data[3]
			).set_author(
				name=f"{ctx.author.name} (@{channel_data[1]})",
				icon_url=channel_data[3]
			), components=[
				ActionRow(
					Button(
						style=ButtonStyle.green,
						label="Continue",
						emoji="<:tick_yes:874284510135607350>",
						custom_id="green"
					),
					Button(
						style=ButtonStyle.red,
						label="Abort",
						emoji="<:tick_no:874284510575996968>",
						custom_id="red"
					)
				)
			]
		)
		file=await ctx.send(
			'Search this video in nsfw channel!' if data[14] == 'y' and not ctx.channel.is_nsfw() else data[3],
			components=[
				ActionRow(
					Button(
						style=ButtonStyle.blurple,
						label=data[4],
						emoji="\U0001f465",
						custom_id="view-button",
						disabled=True
					),
					Button(
						style=ButtonStyle.grey,
						label=channel_data[4],
						emoji="<:user_icon:877535226694352946>",
						custom_id="subs-button",
						disabled=True
					),
					Button(
						style=ButtonStyle.green,
						label=data[5],
						emoji="<:likes:875659362343993404>",
						custom_id="like-button",
						disabled=True
					),
					Button(
						style=ButtonStyle.red,
						label=data[6],
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

		on_click=msg.create_click_listener(timeout=20.0)

		@on_click.not_from_user(ctx.author, cancel_others=True, reset_timeout=False)
		async def _not_from_author(inter):
			await inter.reply(
				embed=discord.Embed(
					description="You are not the member who use this command!",
					color=discord.Color.red()
				), 
					ephemeral=True
				)

		@on_click.matching_id("red")
		async def _red(inter):
			await msg.delete()
			await file.delete()
			await ctx.send(embed=discord.Embed(
				description="Aborting...",
				color=discord.Color.red()
			))

			on_click.kill()

		@on_click.matching_id("green")
		async def _green(inter):
			nonlocal con
			nonlocal cur

			await cur.execute("UPDATE video SET deleted = ? WHERE ID = ?", ("y", ID))

			await con.commit()
			await cur.close()
			await con.close()

			con=await helper.connect("db/channel.db")
			cur=await helper.cursor(con)
			
			await cur.execute("UPDATE channel SET videos = videos - 1 WHERE member_id = ?", (ctx.author.id,))
			await cur.execute("UPDATE channel SET views = ? WHERE member_id = ?", (channel_data[7] - data[4], ctx.author.id))

			await cur.execute("UPDATE channel SET likes = ? WHERE member_id = ?", (channel_data[5] - data[5], ctx.author.id))
			await cur.execute("UPDATE channel SET dislikes = ? WHERE member_id = ?", (channel_data[6] - data[6], ctx.author.id))
			await con.commit()
			await cur.close()
			await con.close()

			await inter.reply(
				type=7,
				content="deleted the video!",
				components=[

				]
			)

	@commands.command("bin", description="View your videos that got deleted!")
	@commands.cooldown(1, 5, commands.BucketType.user)
	async def _bin(self, ctx):
		data=await helper.find_in_video(ctx.author.id, True, mode="all")
		channel_data=await helper.find_in_channel(ctx.author.id)
		info = await helper.find_in_info(ctx.author.id)
		
		if not channel_data:
			await ctx.send(embed=self.channel_error)
			return
		
		if info[2] == 'no':
			await ctx.send(embed=self.login_error)
			return

		if not data:
			await ctx.send(embed=discord.Embed(
				description="All of your video is available!",
				color=discord.Color.red()
			))
			return

		i = 0
		if len(data) > 1: 
			while True:
				raw_date=datetime.datetime.fromtimestamp(int(data[i][10]))
				date_time=raw_date.strftime("%m/%d/%Y")
				msg=await ctx.send(
					embed=discord.Embed(
						title='...' if not ctx.channel.is_nsfw() and data[i][14] == 'y' else data[i][1],
						url='' if not ctx.channel.is_nsfw() and data[i][14] == 'y' else data[i][3],
						description="This video is set to nsfw setting! Make sure to access this video in nsfw channels!" if not ctx.channel.is_nsfw() and data[i][14] == 'y' else data[i][2],
						color=discord.Color.red() if data[i][14] == 'y' else self.embed_color
						).set_footer(
							text=f"Videos {i + 1}/{len(data)} | Date: {date_time} | ID: {data[i][11]}",
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
									custom_id="left-button"
								),
								Button(
									style=ButtonStyle.red,
									label="",
									emoji="<:tick_no:874284510575996968>",
									custom_id="delete-button",
								),
								Button(
									style=ButtonStyle.blurple,
									label="",
									emoji="🔢",
									custom_id="select-button",
								),
								Button(
									style=ButtonStyle.blurple,
									label="",
									emoji="\U000027a1",
									custom_id="right-button"
								)
							)
						]
					)
	
				file=await ctx.send(
					'Search this video in nsfw channel!' if data[i][14] == 'y' and not ctx.channel.is_nsfw() else data[i][3],
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
								style=ButtonStyle.grey,
								label=channel_data[4],
								emoji="<:user_icon:877535226694352946>",
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

				while True:
					try:
						inter = await ctx.wait_for_button_click(lambda inter: inter.author == ctx.author and inter.message.id == msg.id and inter.channel == ctx.channel, timeout=15)
						if inter.author != ctx.author:
							await inter.reply(embed=discord.Embed(
								description="You are not the member who use this command!",
								color=discord.Color.red()
							),
								ephemeral=True
							)
							
						else:
							break

					except asyncio.TimeoutError:
						await ctx.send(embed=discord.Embed(
							title="Timeout!",
							description="I have stop the command due to its long activity!",
							color=discord.Color.red()
						))
						return

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
							color=self.embed_color,
						)
					)
					break

				elif inter.clicked_button.custom_id == "select-button": #Select Button
					try:
						await inter.reply(
							ctx.author.mention, 
							embed=discord.Embed(
								description=f"What video you want to view? You have **{len(data)}** videos",
								color=self.embed_color
							))					
						while True:
							select=await self.bot.wait_for("message", check=lambda x: x.author == ctx.author and x.channel == ctx.channel, timeout=20)
							page=0
							try:
								page=int(select.content)
							except ValueError:
								await asyncio.sleep(0.1)

							if page > len(data):
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
			i = 0
			raw_date=datetime.datetime.fromtimestamp(int(data[i][10]))
			date_time=raw_date.strftime("%m/%d/%Y")
			msg=await ctx.send(
			embed=discord.Embed(
					title='...' if not ctx.channel.is_nsfw() and data[i][14] == 'y' else data[i][1],
					url='' if not ctx.channel.is_nsfw() and data[i][14] == 'y' else data[i][3],
					description="This video is set to nsfw setting! Make sure to access this video in nsfw channels!" if not ctx.channel.is_nsfw() and data[i][14] == 'y' else data[i][2],
					color=discord.Color.red() if data[i][14] == 'y' else self.embed_color
				).set_footer(
					text=f"Videos 1/1 | Date: {date_time} | ID: {data[i][11]}",
					icon_url=channel_data[3]
				).set_author(
					name=f"{ctx.author.name} (@{channel_data[1]})",
					icon_url=channel_data[3]
				)
			)
			file=await ctx.send(
				'Search this video in nsfw channel!' if data[i][14] == 'y' and not ctx.channel.is_nsfw() else data[i][3],
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
							style=ButtonStyle.grey,
							label=channel_data[4],
							emoji="<:user_icon:877535226694352946>",
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
	@commands.command("recent", description="Give you the most recent video! if you dont provided the max videos it will give 10 automaticaly")
	async def _recent(self, ctx, max=10):
		info_data=await helper.find_in_info(ctx.author.id)		
		channel_data=await helper.find_in_channel(ctx.author.id)
		
		if not ctx.author.id in self.bot.owner_ids:
			await ctx.send("This command is under renovation. Comeback after 30 mins!")
			return
		
		if not channel_data:
			await ctx.send(embed=self.channel_error)
			return

		if info_data and info_data[2] == 'no':
			await ctx.send(embed=self.login_error)
			return
		
		loop = True
		i = 0
		
		while True:
			con=await helper.connect("db/video.db")
			cur=await helper.cursor(con)

			con2=await helper.connect("db/channel.db")
			cur2=await helper.cursor(con2)

			await cur.execute("SELECT * FROM video")
			data=await cur.fetchall()
			data=sorted(data, key= lambda x: x[10], reverse=True)
			
			if max > len(data):
				await ctx.send(embed=discord.Embed(
					description=f"Theres only **{len(data)}** video available not **{max}**!",
					color=self.embed_color
				))
				break
				return

			data=data[:max]
			channel_data=await helper.find_in_channel(data[i][0])

			info_con=await helper.connect('db/info.db')
			info_cur=await helper.cursor(info_con)
			info=await helper.find_in_info(ctx.author.id)
			viewed=ast.literal_eval(info[6])
			viewed.append(data[i][11])
			await info_cur.execute("UPDATE info SET viewed = ? WHERE member_id = ?", (str(viewed), ctx.author.id))
			await info_con.commit()
			await info_cur.close()
			await info_con.close()

			try:
				if loop == True:
					old_views=ast.literal_eval(data[i][12])
					if not str(ctx.author.id) in old_views:
						old_views.append(str(ctx.author.id))
						await cur.execute("UPDATE video SET old_views = ? WHERE link = ?", (str(old_views), data[i][3]))
						await cur.execute("UPDATE video SET views = ? WHERE link = ?", (data[i][4] + 1 if int(data[i][0]) != ctx.author.id else data[i][4] + 0, data[i][3]))
						await cur2.execute("UPDATE channel SET views = ? WHERE member_id = ?", (channel_data[7] + 1, data[i][0]))
						
					
					raw_date=datetime.datetime.fromtimestamp(int(data[i][10]))
					date_time=raw_date.strftime("%m/%d/%Y")
					user=await self.bot.fetch_user(channel_data[0])
					msg=await ctx.send(
					embed=discord.Embed(
						title='...' if not ctx.channel.is_nsfw() and data[i][14] == 'y' else data[i][1],
						url='' if not ctx.channel.is_nsfw() and data[i][14] == 'y' else data[i][3],
						description="This video is set to nsfw setting! Make sure to access this video in nsfw channels!" if not ctx.channel.is_nsfw() and data[i][14] == 'y' else data[i][2],
						color=discord.Color.red() if data[i][14] == 'y' else self.embed_color
					).set_footer(
						text=f"Videos {i + 1}/{len(data)} | Date: {date_time} | ID: {data[i][11]}",
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
									custom_id="delete-button",
									disabled=False
								),
								Button(
									style=ButtonStyle.blurple,
									label="",
									emoji="\U000027a1",
									custom_id="right-button"
								)
							)
						]
					) 
					file=await ctx.send(
						'Search this video in nsfw channel!' if not ctx.channel.is_nsfw() and data[i][14] == 'y' else data[i][3],
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
									style=ButtonStyle.grey,
									label=channel_data[4],
									emoji="<:user_icon:877535226694352946>",
									custom_id="subs-button",
									disabled=True if str(ctx.author.id) in ast.literal_eval(channel_data[11]) else False
								),
								Button(
									style=ButtonStyle.green,
									label=data[i][5],
									emoji="<:likes:875659362343993404>",
									custom_id="like-button",
									disabled=True if str(ctx.author.id) in data[i][7] else False
								),
								Button(
									style=ButtonStyle.red,
									label=data[i][6],
									emoji="<:dislikes:875659362264309821>",
									custom_id="dislike-button",
									disabled=True if str(ctx.author.id) in data[i][8] else False
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

				while True:
					try:
						inter = await ctx.wait_for_button_click(lambda inter: inter.message.id == msg.id or inter.message.id == file.id and inter.channel == ctx.channel, timeout=100)	
						if inter.author != ctx.author:
							await inter.reply(embed=discord.Embed(
								description="You are not the member who use this command!",
								color=discord.Color.red()
							), 
								ephemeral=True
							)
							
						else:
							break

					except asyncio.TimeoutError:
						await msg.delete()
						await file.delete()
						await ctx.send(embed=discord.Embed(
							title="Timeout",
							description="I have stop the command due to its long activity!",
							color=discord.Color.red()
						))
						return

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

					await cur.close()
					await cur2.close()
					await con.close()
					await con2.close()

				elif button_id == "delete-button": #Delete Button
					await msg.delete()
					await file.delete()
					await ctx.send(embed=discord.Embed(
							description=f"{ctx.author.mention} thanks for using Tango bot :blush:",
							color=self.embed_color,
						)
					)
					
					await cur.close()
					await cur2.close()
					await con.close()
					await con2.close()
					break

				elif button_id == "subs-button":
					info_con=await helper.connect('db/info.db')
					info_cur=await helper.cursor(info_con)
					info=await info_cur.execute("SELECT subscribed FROM info WHERE member_id = ?", (ctx.author.id,))
					info=await info.fetchone()
					info_data=ast.literal_eval(info[0])
					info_data.append(data[i][11])
					await info_cur.execute("UPDATE info SET subscribed = ? WHERE member_id = ?", (str(info_data), ctx.author.id))
					await info_con.commit()
					await info_cur.close()
					await info_con.close()

					subs=ast.literal_eval(channel_data[11])
					if not str(ctx.author.id) in subs:
						subs.append(str(ctx.author.id))
	
						await inter.send(embed=discord.Embed(
							description=f"{ctx.author.mention} Sub the channel!",
							color=self.embed_color
						),
							ephemeral=True
						)
		
						await cur2.execute("UPDATE channel SET subscribers = subscribers + 1 WHERE member_id = ?", (channel_data[0],))
						await cur2.execute("UPDATE channel SET old_subs = ? WHERE member_id = ?", (str(subs), channel_data[0]))
						await con2.commit()

					await file.edit(
						content=data[i][3],
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
									style=ButtonStyle.grey,
									label=channel_data[4] + 1,
									emoji="<:user_icon:877535226694352946>",
									custom_id="subs-button",
									disabled=True
								),
								Button(
									style=ButtonStyle.green,
									label=data[i][5],
									emoji="<:likes:875659362343993404>",
									custom_id="like-button",
									disabled=True if str(ctx.author.id) in ast.literal_eval(data[i][7]) else False 
								),
								Button(
									style=ButtonStyle.red,
									label=data[i][6],
									emoji="<:dislikes:875659362264309821>",
									custom_id="dislike-button",
									disabled=True if str(ctx.author.id) in ast.literal_eval(data[i][8]) else False
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

					loop = False
					await cur2.close()
					await cur.close()
					await con2.close()
					await con.close()

				elif button_id == "like-button": #Like Button
					likes=ast.literal_eval(data[i][7]) #list member who liked
					dislikes=ast.literal_eval(data[i][8]) #list member who disliked
					await cur2.execute("UPDATE channel SET likes = ? WHERE member_id = ?", (channel_data[5] + 1, data[i][0]))


					if not str(ctx.author.id) in likes:
						likes.append(str(ctx.author.id))
						
		
					if str(ctx.author.id) in dislikes:
						dislikes.remove(str(ctx.author.id))
						await cur.execute("UPDATE video SET old_dislikes = ? WHERE link = ?", (str(dislikes), str(data[i][3])))
						await cur.execute("UPDATE video SET dislikes = ? WHERE link = ?", (data[i][6] - 1, str(data[i][3])))
						await cur2.execute("UPDATE channel SET dislikes = ? WHERE member_id = ?", (channel_data[6] - 1, data[i][0]))
					
					
					await cur.execute("UPDATE video SET old_likes = ? WHERE link = ?", (str(likes), str(data[i][3])))
					await cur.execute("UPDATE video SET likes = ? WHERE link = ?", (int(data[i][5]) + 1, str(data[i][3])))

					await con.commit()
					await con2.commit()

					await inter.send(embed=discord.Embed(
						description=f"{ctx.author.mention} Liked this video!",
						color=self.embed_color
					),
						ephemeral=True
					)

					await file.edit(
						content='Search this video in nsfw channel!' if not ctx.channel.is_nsfw() and data[i][14] == 'y' else data[i][3],
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
									style=ButtonStyle.grey,
									label=channel_data[4],
									emoji="<:user_icon:877535226694352946>",
									custom_id="subs-button",
									disabled=True if str(ctx.author.id) in ast.literal_eval(channel_data[11]) else False
								),
								Button(
									style=ButtonStyle.green,
									label=data[i][5] + 1,
									emoji="<:likes:875659362343993404>",
									custom_id="like-button",
									disabled=True
								),
								Button(
									style=ButtonStyle.red,
									label=data[i][6] - 1 if str(ctx.author.id) in ast.literal_eval(data[i][8]) else data[i][5],
									emoji="<:dislikes:875659362264309821>",
									custom_id="dislike-button",
									disabled=False
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
					
					loop = False
					await cur.close()
					await cur2.close()
					await con.close()
					await con2.close()
							
				elif button_id == "dislike-button": #Dislike Button
					likes=ast.literal_eval(data[i][7])
					dislikes=ast.literal_eval(data[i][8])
					await cur2.execute("UPDATE channel SET dislikes = ? WHERE member_id = ?", (channel_data[6] + 1, data[i][0]))

					if not str(ctx.author.id) in dislikes:
						dislikes.append(str(ctx.author.id))
						
					if str(ctx.author.id) in likes:
						likes.remove(str(ctx.author.id))
						await cur.execute("UPDATE video SET old_likes = ? WHERE link = ?", (str(likes), str(data[i][3])))
						await cur.execute("UPDATE video SET likes = ? WHERE link = ?", (data[i][5] - 1, str(data[i][3])))
						await cur2.execute("UPDATE channel SET likes = ? WHERE member_id = ?", (channel_data[5] - 1, data[i][0]))
					
					
					
					await cur.execute("UPDATE video SET old_dislikes = ? WHERE link = ?", (str(dislikes), str(data[i][3])))
					await cur.execute("UPDATE video SET dislikes = ? WHERE link = ?", (int(data[i][6]) + 1, str(data[i][3])))
					
					
					await con.commit()
					await con2.commit()

					await inter.send(embed=discord.Embed(
						description=f"{ctx.author.mention} Disliked this video!",
						color=self.embed_color
					),
						ephemeral=True
					)
					
					await file.edit(
						content='Search this video in nsfw channel!' if not ctx.channel.is_nsfw() and data[i][14] == 'y' else data[i][3],
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
									style=ButtonStyle.grey,
									label=channel_data[4],
									emoji="<:user_icon:877535226694352946>",
									custom_id="subs-button",
									disabled=True if str(ctx.author.id) in ast.literal_eval(channel_data[11]) else False
								),
								Button(
									style=ButtonStyle.green,
									label=data[i][5] - 1 if str(ctx.author.id) in ast.literal_eval(data[i][7]) else data[i][5],
									emoji="<:likes:875659362343993404>",
									custom_id="like-button",
									disabled=False
								),
								Button(
									style=ButtonStyle.red,
									label=data[i][6] + 1,
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
					loop = False
					await cur.close()
					await cur2.close()
					await con.close()
					await con2.close()

			except Exception as e:
				raise e
		 
	@commands.command("history", description="Show a list of videos that you viewed before! If you dont provided max_video, it will automatically send 10!")
	async def _history(self, ctx, max_video=10):
		con=await helper.connect("db/info.db")
		cur=await helper.cursor(con)
		info=await helper.find_in_info(ctx.author.id)
		
		if not info:
			await ctx.send(embed=self.channel_error)
			return

		if info[2] == 'no':
			await ctx.send(embed=self.login_error)
			return

		channel_data=await helper.find_in_channel(ctx.author.id)
		await cur.execute("SELECT * FROM info WHERE member_id = ?", (ctx.author.id,))
		history=await cur.fetchall()
		await cur.close()
		await con.close()
		
		data=ast.literal_eval(history[0][6])
		if max_video > len(data):
			await ctx.send(embed=discord.Embed(
				description=f"There's is Nothing to find in your histroy! History get clear every 30 minutes",
				color=self.embed_color
			).set_footer(
				text="Use p!help history for more info about the command!",
				icon_url=ctx.author.avatar_url
			))
			return

		con=await helper.connect('db/video.db')
		cur=await helper.cursor(con)
		raw_data=[]

		for id in data:
			raw_data.insert(0, id) # Reverse the list without using sort or sorted 

		data=[]
		
		for id in raw_data[:max_video]:
			await cur.execute("SELECT * FROM video WHERE ID = ?", (id,))
			video_=await cur.fetchone()
			data.append(video_)

		video=len(data)
		await cur.close()
		await con.close()

		i = 0
		while True:
			raw_date=datetime.datetime.fromtimestamp(int(data[i][10]))
			date_time=raw_date.strftime("%m/%d/%Y")
			msg=await ctx.send(
				embed=discord.Embed(
					title='...' if not ctx.channel.is_nsfw() and data[i][14] == 'y' else data[i][1],
					url='' if not ctx.channel.is_nsfw() and data[i][14] == 'y' else data[i][3],
					description="This video is set to nsfw setting! Make sure to access this video in nsfw channels!" if not ctx.channel.is_nsfw() and data[i][14] == 'y' else data[i][2],
					color=discord.Color.red() if data[i][14] == 'y' else self.embed_color
					).set_footer(
						text=f"Videos {i + 1}/{video} | Date: {date_time} | ID: {data[i][11]}",
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
								custom_id="left-button"
							),
							Button(
								style=ButtonStyle.red,
								label="",
								emoji="<:tick_no:874284510575996968>",
								custom_id="delete-button",
							),
							Button(
								style=ButtonStyle.blurple,
								label="",
								emoji="🔢",
								custom_id="select-button",
							),
							Button(
								style=ButtonStyle.blurple,
								label="",
								emoji="\U000027a1",
								custom_id="right-button"
							)
						)
					]
				)

			file=await ctx.send(
				'Search this video in nsfw channel!' if data[i][14] == 'y' else data[i][3],
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
							style=ButtonStyle.grey,
							label=channel_data[4],
							emoji="<:user_icon:877535226694352946>",
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

			while True:
				try:
					inter = await ctx.wait_for_button_click(lambda inter: inter.author == ctx.author and inter.message.id == msg.id and inter.channel == ctx.channel, timeout=15)
					if inter.author != ctx.author:
						await inter.reply(embed=discord.Embed(
							description="You are not the member who use this command!",
							color=discord.Color.red()
						),
							ephemeral=True
						)
						
					else:
						break

				except asyncio.TimeoutError:
						await ctx.send(embed=discord.Embed(
							title="Timeout!",
							description="I have stop the command due to its long activity!",
							color=discord.Color.red()
						))
						return
				
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
						color=self.embed_color,
					)
				)
				break

			elif inter.clicked_button.custom_id == "select-button": #Select Button
				try:
					await inter.reply(
						ctx.author.mention, 
						embed=discord.Embed(
							description=f"What video you want to view? You have **{video}** videos",
							color=self.embed_color
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
		
		

	
@commands.command("reupload")
async def _reupload(self, ctx, video_ID):
	con=await helper.connect("db/video.db")
	cur=await helper.cursor(con)

	channel=await helper.find_in_channel(ctx.author.id)
	info=await helper.find_in_info(ctx.author.id)
	
	await cur.execute("SELECT * FROM video WHERE ID = ?", (video_ID,))
	data=await cur.fetchone()

	if not channel:
		await ctx.send(embed=self.channel_error)
		return

	if info[2] == 'no':
		await ctx.send(embed=self.login_error)
		return

	if not data:
		await ctx.send(embed=discord.Embed(
			description="You put a wrong ID!",
			color=discord.Color.red()
		))
		return

	if data[13] == 'n':
		await ctx.send(embed=discord.Embed(
			description="That video is already available!",
			color=discord.Color.red()
		))
		return

	if data[0] != ctx.author.id:
		await ctx.send(embed=discord.Embed(
			description="Your not the owner who deleted this video!",
			color=discord.Color.red()
		))
		return

	try:
		await cur.execute("UPDATE video SET deleted = ? WHERE ID = ?", ('n', video_ID))
		await con.commit()
		await cur.close()
		await con.close()

		await ctx.send(f"You reuploaded that video! Check it using `p!view {video_ID}`")

	except Exception as e:
		raise e 	

		



def setup(bot):
	bot.add_cog(social(bot))