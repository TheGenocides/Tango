import discord
import helper
import os
import difflib
import datetime
import traceback

#======================

from discord.ext import commands
from dislash import SlashClient, Option, Type, InteractionClient

class Tango(commands.Bot):
	def __init__(self):#Bubble-gum blue, Sakura pink
		self.color=[0xAFEEEE, 0xFFB6C1]
		super().__init__(
			command_prefix=commands.when_mentioned_or("p!"),
			help_command=HelpPage(),
			intents=discord.Intents.all(),
			allowed_mentions=discord.AllowedMentions(everyone=False, users=True, roles=False, replied_user=True),
			case_insensitive=True,
			activity=discord.Activity(name="10 Accounts | p!help", type=discord.ActivityType.watching),
			status=discord.Status.idle,
			owner_ids=[685082846993317953, 687943803604303872, 806725119917162527]
		)


	async def on_message(self, msg):
		if msg.content == "<@!806725119917162527>":
			await msg.reply(
				embed=discord.Embed(
					description="Hello there, my prefix is `p!`",
					color=discord.Color.red()
				)
			)

		await self.process_commands(msg)

	async def on_ready(self):
		await self.wait_until_ready()
		slash=InteractionClient(self)

		db=await helper.connect("db/channel.db")
		cur=await helper.cursor(db)
		await cur.execute("""
				CREATE TABLE IF NOT EXISTS channel (
					member_id integer,
					channel text,
					description text,
					banner text,
					subscribers integer,
					likes integer,
					dislikes integer,
					views integer,
					videos integer,
					verified_channel text,
					money integer,
					old_subs text
		)""")

		db2=await helper.connect("db/info.db")
		cur2=await helper.cursor(db2)
		await cur2.execute("""
				CREATE TABLE IF NOT EXISTS info (
					member_id integer,
					gender text,
					verified text,
					email text,
					password text,
					age text,
					viewed text,
					subscribed text,
					liked text,
					disliked text
		)""") 

		db3=await helper.connect("db/video.db")
		cur3=await helper.cursor(db3)
		await cur3.execute("""
				CREATE TABLE IF NOT EXISTS video (
					member_id integer, 
					title text,
					description text,
					link text,
					views integer,
					likes integer,
					dislikes integer,
					old_likes text,
					old_dislikes text,
					content_type text,
					date integer,
					ID text,
					old_views text,
					deleted text,
					nsfw text,
					comments integer
		)""")

		db4=await helper.connect('db/comment.db')
		cur4=await helper.cursor(db4)
		await cur4.execute("""CREATE TABLE IF NOT EXISTS comments(
			commenter_id integer, 
			video_id integer, 
			content text, 
			comment_id integer, 
			date integer
		)""")

		await db.commit()
		await db2.commit()
		await db3.commit()
		await db4.commit()
		await cur.close()
		await cur2.close()
		await cur3.close()
		await cur4.close()
		await db.close()
		await db2.close()
		await db3.close()
		await db4.close()
		print("Im online :)")
		

	async def on_command_error(self, ctx, error):
 
		NotOwner="<Not Owner>"
		if isinstance(error, (commands.MissingRole, commands.MissingAnyRole)):
			print(error.__class__)
			roles=[ctx.guild.get_role(role).mention for role in error.missing_roles] if isinstance(error, commands.errors.MissingAnyRole) else ctx.guild.get_role(int(error.missing_role)).mention
			em=discord.Embed(
				title="Missing Roles",
				description=f"You are missing {roles}" if isinstance(error, commands.MissingRole) else f"You are missing one of these roles {', '.join(roles[:-1])}, and {roles[-1]}",
				color=discord.Color.red()
			)

			em.set_author(
				name=ctx.author,
				icon_url=ctx.author.avatar_url
			)
			
			em.set_footer(
				text=f"Requested By {ctx.author} • Use p!help {ctx.invoked_with} for more info about the command!",
				icon_url=ctx.author.avatar_url
			)

			await ctx.send(embed=em)
			return

		elif isinstance(error, (commands.errors.MissingPermissions, commands.errors.MissingRequiredArgument)):
			em=discord.Embed(
				title="You are Missing Some Permission(s)" if isinstance(error, commands.errors.MissingPermissions) else "You are Missing A Required Argument(s)",
				description=f"You are missing {'This Permission:' if len(error.missing_perms) == 1 else 'These Permission(s):'} {', '.join(error.missing_perms[0].replace('_', ' ') if len(error.missing_perms) == 1 else x.replace('_', ' ') for x in error.missing_perms)}" if isinstance(error, commands.errors.MissingPermissions) else f"You are missing '{error.param}' argument",
				color=discord.Color.red()
			)

			em.set_author(
				name=ctx.author,
				icon_url=ctx.author.avatar_url
			)
			
			em.set_footer(
				text=f"Requested By {ctx.author} • Use p!help {ctx.invoked_with} for more info about the command!",
				icon_url=ctx.author.avatar_url
			)

			await ctx.send(embed=em)
			return
		
		elif isinstance(error, commands.CommandInvokeError):
			org=getattr(error, "original", error)
			if isinstance(org, discord.errors.HTTPException):
				pass

			else:
				raise error

		elif isinstance(error, commands.CommandNotFound):
			possi=difflib.get_close_matches(ctx.invoked_with.lower(), ['uptime', 'ping', 'news', 'info', "start", "channel", "post", "videos", "search", "setting", 'login','profile', 'view', 'comment', 'logout', 'delete']) 
			em=discord.Embed(
				title="Command Not Found",
				description=f"No command called `{ctx.invoked_with}` did you mean `{', '.join(possi if possi else '.....')}`",
				color=discord.Color.red()
			).set_author(
				name=ctx.author,
				icon_url=ctx.author.avatar_url
			).set_footer(
				text=f"Requested By {ctx.author} • Use p!help for more info about all commands!",
				icon_url=ctx.author.avatar_url
			)

			await ctx.send(embed=em)
			return
		elif isinstance(error, commands.CommandOnCooldown):
			msg = f'**Command Still on cooldown**, please try again in **{error.retry_after:.2f}s** or wait untill this message got deleted!'
			await ctx.send(
				embed=discord.Embed(
				title="Cooldown!",
				description=msg,
				color=discord.Color.red()
			).set_author(
				name=ctx.author,
				icon_url=ctx.author.avatar_url
			).set_footer(
				text=f"Requested By {ctx.author} • Use p!help for more info about all commands!",
				icon_url=ctx.author.avatar_url
			), delete_after=error.retry_after
		)

		else:
			await ctx.send(embed=discord.Embed(
				title="Error",
				description="An unexpected error has occured! I have notify my owner to fix this error!",
				color=discord.Color.red()
			))

			channel=self.get_channel(879610856588075029)
			tb = "".join(traceback.format_exception(type(error), error, error.__traceback__))
			await channel.send(
				"An Error Has Occured",	
				embed=discord.Embed(
				description=f"```py\n{tb}\n```",
				color=discord.Color.red()
			))
			raise error
			


	def _run_(self, token):
		for fn in os.listdir("./cogs"):
			if fn.endswith(".py"):
				self.load_extension(f"cogs.{fn[:-3]}")
		print(f"Log in as Tango#8351")
		print("Discord.Python Version :", discord.__version__)
		print("Ratelimit: ", self.is_ws_ratelimited())
		self.load_extension("jishaku")
		self.run(token)	

def setup(self):
	self.add_cog(Tango(self))

class HelpPage(commands.HelpCommand):
	def get_ending_note(self, category: bool):
		return f"Use {self.clean_prefix}{self.invoked_with} [{'Category' if category == True else 'command'}] for more info on {'all commands' if category == True else 'the command'}"

	def get_command_signature(self, command):
		return command.signature if command.signature else " "

	async def send_bot_help(self, mapping):
		cog_description={"owner": "These command can only use by one of the owner of the bot.", "fun": "Commands that can be use by all members without any specific permissions or roles.", "social": "Social is a command category that contain commands that related to Social Media!", "jishaku": "Jishaku commands", "information": "Commands that have all information that you need about Tango bot"}
		
		emojis={"owner": "<:Tango:878902180856352848>", "fun": "🤡", "social": "<:follow:879722735788519444>", "jishaku": "⚙️", "information": "🛑"}
		em=discord.Embed(
			title="HelpCommand",
			description="Hello there, I'm Tango! A discord bot with Social Media Functions that lets you connect with others through their videos! Gain followers, Post your favorite video and get tons of views! Bored? Use our search command and find funny videos! Support creators by liking their video and subscribe, be sure not to dislikes them!\n\n**Select A Category:**",
			color=discord.Color.from_rgb(136, 223 ,251)
		)
		for cog, cmd in mapping.items():
			att=getattr(cog, "qualified_name", "No Category")
			if att != "No Category" and att != "Jishaku":
				all_commands=cog.get_commands()
				em.add_field(
					name=f"{emojis[att]} {att} [{len(all_commands)}]",
					value=cog_description[att],
					inline=False
				)
			
			else:
				pass

		em.set_author(
			name=self.context.author,
			icon_url=self.context.author.avatar_url
		)
		em.set_footer(
			text=self.get_ending_note(True) + " Or click the buttons to move the page!",
			icon_url=self.context.author.avatar_url
		)
		channel=self.get_destination()
		await channel.send(embed=em)

	async def send_cog_help(self, cog):
		em=discord.Embed(
			title=f"{cog.qualified_name}'s commands",
			description="",
			color=discord.Color.from_rgb(136, 223 ,251)
		)

		for cms in cog.get_commands():
			com=cms.name
			em.description += f"`{com}`, "

		em.set_author(
			name=self.context.author,
			icon_url=self.context.author.avatar_url
		)
		em.set_footer(
			text=self.get_ending_note(False),
			icon_url=self.context.author.avatar_url
		)
		channel=self.get_destination()
		await channel.send(embed=em)
	
	async def send_group_help(self, gr):
		channel=self.get_destination()
		cmds=list(x.name for x in gr.commands)
		sig=gr.signature
		name=gr.qualified_name
		description={"anime": "For getting info about anime!"}
		em=discord.Embed(
			title=name,
			description=description[name],
			color=discord.Color.from_rgb(136, 223 ,251)
		).add_field(
			name="Syntax",
			value=f"{self.clean_prefix}{name} {sig}",
			inline=True
		).add_field(
			name="Sub-Commands",
			value=', '.join([x for x in cmds]),
			inline=True
		).set_author(
			name=self.context.author,
			icon_url=self.context.author.avatar_url
		).set_footer(
			text=f"Use p!help {name} [Sub-Commands] for more info about the Sub-Commands",
			icon_url=self.context.author.avatar_url
		)
		
		await channel.send(embed=em)

	async def send_command_help(self, command):
		channel=self.get_destination()
		desc=command.description
		aliases=command.aliases

		if aliases == []:
			aliases.append("This command dont have aliases")
	
		em=discord.Embed(
			title=command.name,
			description=desc,
			color=discord.Color.from_rgb(136, 223 ,251)
		).add_field(
			name="Syntax",
			value=f"{self.clean_prefix}{command.qualified_name} {self.get_command_signature(command)}",
			inline=True
		).add_field(
			name="Aliases",
			value=', '.join(x for x in aliases if not x.startswith(" ")),
			inline=True
		).set_author(
			name=self.context.author,
			icon_url=self.context.author.avatar_url
		).set_footer(
			text=f"Requested by {self.context.author}",
			icon_url=self.context.author.avatar_url
		)
		
		await channel.send(embed=em)

	async def command_not_found(self, error):
		channel = self.get_destination()
		possi=difflib.get_close_matches(error.lower(), ['uptime', 'ping', 'news', 'info', "start", "channel", "post", "videos", "search", "setting", 'login','profile', 'view', 'comment', 'logout', 'delete'])
		category=difflib.get_close_matches(error.title(), ["owner", "fun", "social", "information"])

		if category and not possi:
			embed = discord.Embed(
				title=f"No Category called '{error}' ",
				description=f"Did you mean `{', '.join(category)}`",
				color=discord.Color.red() 
			).set_author(
				name=self.context.author,
				icon_url=self.context.author.avatar_url
			).set_footer(
				text=f"Use {self.clean_prefix}{self.invoked_with} for more info about all commands",
				icon_url=self.context.author.avatar_url
			)
			await channel.send(embed=embed)
		
		elif possi and not category:
			embed = discord.Embed(
				title=f"No Command called '{error}' ",
				description=f"Did you mean `{', '.join(possi)}`",
				color=discord.Color.red() 
			).set_author(
				name=self.context.author,
				icon_url=self.context.author.avatar_url
			).set_footer(
				text=f"Use {self.clean_prefix}{self.invoked_with} for more info about all commands",
				icon_url=self.context.author.avatar_url
			)
			await channel.send(embed=embed)

		else:
			embed = discord.Embed(
				title=f"No Command called '{error}' ",
				description=f"Did you mean `.....`",
				color=discord.Color.red() 
			).set_author(
				name=self.context.author,
				icon_url=self.context.author.avatar_url
			).set_footer(
				text=f"Use {self.clean_prefix}{self.invoked_with} for more info about all commands",
				icon_url=self.context.author.avatar_url
			)
			await channel.send(embed=embed)


#Context Menu Command

slash=SlashClient(Tango())
guild_ids=[858312394236624957, 843610787867525120]


@slash.user_command(name="Show Your Profile!", guild_ids=guild_ids)
async def _profile(inter):
	member=inter.author
	data=await helper.find_in_channel(member.id)
	info=await helper.find_in_info(member.id)
	
	if not data or not info:
		await inter.respond(
			embed=discord.Embed(
			description=f"{inter.author.name} haven't made a channel, Use p!start command!",
			color=discord.Color.red()
			)
		)
		return

	
	await inter.respond(
			embed=discord.Embed(
				title="Profile Menu!",
				description=data[2],
				color=discord.Color.from_rgb(213, 240, 213),
				timestamp=datetime.datetime.utcnow()
				).set_author(
					name=f"{inter.author.name} (@{data[1]})",
					icon_url=data[3]
				).set_footer(
					text=f"Source: @{data[1]} | ID: {inter.author.id}",
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
					name="📧 Email",
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

@slash.message_command(name="Show User Profile!", guild_ids=guild_ids)
async def _Profile(inter):
	member=inter.message.author
	data=await helper.find_in_channel(member.id)
	info=await helper.find_in_info(member.id)
	
	if not data:
		await inter.respond(
			embed=discord.Embed(
			description=f"{inter.author.name} haven't made a channel, Use p!start command! (Start command is under renovation)",
			color=discord.Color.red()
			)
		)
		return

	if not info:
		await inter.respond(
			embed=discord.Embed(
			color=discord.Color.red()
		).set_footer(
			text="You havent made a video, use p!post command!"
		)
	)
		
	
	await inter.respond(
			embed=discord.Embed(
				title="Profile Menu!",
				description=data[2],
				color=discord.Color.from_rgb(213, 240, 213),
				timestamp=datetime.datetime.utcnow()
				).set_author(
					name=f"{inter.author.name} (@{data[1]})",
					icon_url=data[3]
				).set_footer(
					text=f"Source: @{data[1]} | ID: {inter.author.id}",
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
					name="📧 Email",
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

@slash.command(
    name="echo",
	description="Echo word that you specified",
    options=[
        Option("word", "Specify a word that will get send", Type.STRING, required=True)
    ],
	guild_ids=guild_ids
)
async def echo(inter, *,word):
	await inter.reply(word, allowed_mentions=discord.AllowedMentions(everyone=False, users=False, roles=False, replied_user=True))

@slash.command(
    name="help",
	description="A short way to get access for help command",
	guild_ids=guild_ids
)
async def help(inter):
	cog_description={"Owner": "These commands can only use by one of the owner of the bot.", "Fun": "Commands that can be use by all members without any specific permissions or roles.", "Social": "Social is a group of commands that contain most of the commands that other can use!", "Jishaku": "Jishaku commands", "Information": "Commands that have all information that you need about Tango bot"}

	categories=["Owner", "Fun", "Social", "Information"]
		
	emojis={"Owner": "👑", "Fun": "🤡", "Social": "🗨️", "Jishaku": "⚙️", "Information": "🛑"}

	num_commands={"Owner": "4", "Fun": "2", "Social": "6", "Jishaku": "1", "Information": "2"}

	em=discord.Embed(
		title="HelpCommand",
		description="Hello there, im Tango. A fun bot with a social media functions! Gain followers, million of views, and become the most followed channel! Post your meme and messages in community post! Post your video and get ton of review! All seen across multiple country!\n\n**Select A Category:**",
		color=discord.Color.from_rgb(136, 223 ,251)
	)
	
	for x in categories:
		em.add_field(
			name=f"{emojis[x]} {x} [{num_commands[x]}]",
			value=cog_description[x],
			inline=False
		)

	await inter.reply(embed=em)