import discord
import helper
import os
import difflib
import datetime
import helper

#======================

from discord.ext import commands
from dislash import SlashClient, Option, Type

class Tango(commands.Bot):
	def __init__(self):
		super().__init__(
			command_prefix=commands.when_mentioned_or("p!"),
			help_command=HelpPage(),
			intents=discord.Intents.all(),
			allowed_mentions=discord.AllowedMentions(everyone=False, users=True, roles=False, replied_user=True),
			case_insensitive=True,
			activity=discord.Activity(name="A Media Social >:)", type=discord.ActivityType.competing),
			status=discord.Status.idle,
			owner_ids=[685082846993317953, 687943803604303872]
		)

	async def on_disconnect(self):
		channel=self.get_channel(875023982418599956)
		owner=self.get_user(self.owner_ids[0])

		msg=await channel.send(
			owner.mention,
			embed=discord.Embed(
				title="<:dnd:873411447416320050> Disconnect",
				description="I got disconnected <:dnd:873411447416320050>",
				color=discord.Color.red(),
				timestamp=datetime.datetime.utcnow()
			)
		)
		await msg.publish()

	async def on_connect(self):
		channel=self.get_channel(875023982418599956)
		owner=self.get_user(self.owner_ids[0])
		msg=await channel.send(
			owner.mention,
			embed=discord.Embed(
				title="<:Online:873411447479214110> Online",
				description="I am back online <:Online:873411447479214110>",
				color=discord.Color.green(),
				timestamp=datetime.datetime.utcnow()
			)
		)
		await msg.publish()

	async def on_ready(self):
		await self.wait_until_ready()
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
					money integer
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
					age text
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
					date integer
		)""")

		await db.commit()
		await db2.commit()
		await db3.commit()
		

	async def on_command_error(self, ctx, error):
		CommandNotFound="<class 'discord.ext.commands.errors.CommandNotFound'>"
		if isinstance(error, (commands.MissingRole, commands.MissingAnyRole)):
			print(error.__class__)
			roles=[ctx.guild.get_role(role).mention for role in error.missing_roles] if isinstance(error, commands.errors.MissingAnyRole) else ctx.guild.get_role(int(error.missing_role)).mention
			em=discord.Embed(
				title="Missing Roles",
				description=f"You are missing {roles}" if isinstance(error, commands.MissingRole) else f"You are missing one of these roles {', '.join(roles[:-1])}, and {roles[-1]}",
				color=discord.Color.red()
			)

			em.set_author(
				name=f"By {ctx.author}",
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
				name=f"By {ctx.author}",
				icon_url=ctx.author.avatar_url
			)
			
			em.set_footer(
				text=f"Requested By {ctx.author} • Use p!help {ctx.invoked_with} for more info about the command!",
				icon_url=ctx.author.avatar_url
			)

			await ctx.send(embed=em)
			return
		else:
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
		cog_description={"Owner": "These command can only use by one of the owner of the bot.", "Fun": "Commands that can be use by all members without any specific permissions or roles.", "Social": "Social is a group of commands that contain most of the commands that other can use!", "Jishaku": "Jishaku commands", "Information": "Commands that have all information that you need about Tango bot"}
		
		emojies={"Owner": "👑", "Fun": "🤡", "Social": "🗨️", "Jishaku": "⚙️", "Information": "🛑"}
		em=discord.Embed(
			title="HelpCommand",
			description="Hello there, im Tango. A fun bot with a social media functions! Gain followers, million of views, and become the most followed channel! Post your meme and messages in community post! Post your video and get ton of review!. All seen across multiple country!\n\n**Select A Category:**",
			color=discord.Color.orange()
		)
		for cog, cmd in mapping.items():
			att=getattr(cog, "qualified_name", "No Category")
			if att != "No Category" and att != "Jishaku":
				all_commands=cog.get_commands()
				em.add_field(
					name=f"{emojies[att]} {att} [{len(all_commands)}]",
					value=cog_description[att],
					inline=False
				)
			
			else:
				pass

		em.set_author(
			name=f"By {self.context.author}",
			icon_url=self.context.author.avatar_url
		)
		em.set_footer(
			text=self.get_ending_note(True),
			icon_url=self.context.author.avatar_url
		)
		channel=self.get_destination()
		await channel.send(embed=em)

	async def send_cog_help(self, cog):
		em=discord.Embed(
			title=f"{cog.qualified_name}'s commands",
			description="",
			color=discord.Color.orange()
		)

		for cms in cog.get_commands():
			com=cms.name
			em.description += f"`{com}`, "

		em.set_author(
			name=f"By {self.context.author}",
			icon_url=self.context.author.avatar_url
		)
		em.set_footer(
			text=self.get_ending_note(False),
			icon_url=self.context.author.avatar_url
		)
		channel=self.get_destination()
		await channel.send(embed=em)
	
	async def send_command_help(self, command):
		channel=self.get_destination()
		desc=getattr(command, 'description', "This command dont have a description")
		aliases=getattr(command, "aliases", "This command dont have aliases")
		if aliases == []:
			aliases.append("This command dont have aliases")
		

		em=discord.Embed(
			title=command.name,
			description=desc,
			color=discord.Color.orange()
		).add_field(
			name="Syntax",
			value=f"{self.clean_prefix}{command.qualified_name} {self.get_command_signature(command)}",
			inline=True
		).add_field(
			name="Aliases",
			value=', '.join(x for x in aliases if not x.startswith(" ")),
			inline=True
		).set_author(
			name=f"By {self.context.author}",
			icon_url=self.context.author.avatar_url
		).set_footer(
			text=f"Requested by {self.context.author}",
			icon_url=self.context.author.avatar_url
		)
		
		await channel.send(embed=em)

	async def command_not_found(self, error):
		channel = self.get_destination()
		commands=['uptime', 'ping', 'idea', 'info', "start", "channel", "post", "videos", "search", "setting"]
		possi=difflib.get_close_matches(error.lower(), commands)
		category=difflib.get_close_matches(error.title(), ["Owner", "Fun", "Social", "Information"])
		if category and not possi:
			embed = discord.Embed(
				title=f"No Category called '{error}' ",
				description=f"Did you mean `{', '.join(category)}`",
				color=discord.Color.red() 
			).set_author(
				name=f"By {self.context.author}",
				icon_url=self.context.author.avatar_url
			).set_footer(
				text=f"Use {self.clean_prefix}{self.invoked_with} for more info about all commands",
				icon_url=self.context.author.avatar_url
			)
			await channel.send(embed=embed)
		
		elif possi and not category:
			embed = discord.Embed(
				title=f"No Command called '{error}' ",
				description=f"Did you mean `{', '.join(possi) if possi else '.....'}`",
				color=discord.Color.red() 
			).set_author(
				name=f"By {self.context.author}",
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
				name=f"By {self.context.author}",
				icon_url=self.context.author.avatar_url
			).set_footer(
				text=f"Use {self.clean_prefix}{self.invoked_with} for more info about all commands",
				icon_url=self.context.author.avatar_url
			)
			await channel.send(embed=embed)

	async def send_error_message(self, error):
		channel = self.get_destination()
		commands=['uptime', 'ping', 'idea', 'info', "start", "channel", "post", "videos", "search", "setting"]
		possi=difflib.get_close_matches(error.lower(), commands)
		category=difflib.get_close_matches(error.title(), ["Owner", "Fun", "Social", "Information"])
		if possi or category:
			return
		embed = discord.Embed(
			title="Error",
			description=error,
			color=discord.Color.red() 
		).set_author(
			name=self.context.author,
			icon_url=self.context.author.avatar_url
		).set_footer(
			text=self.get_ending_note(False),
			icon_url=self.context.author.avatar_url
		)
		await channel.send(embed=embed)

#Slash Command

slash=SlashClient(Tango())
guild_ids=[858312394236624957, 843610787867525120]


@slash.user_command(name="Profile", guild_ids=guild_ids)
async def _profile(inter):
	member=inter.author
	data=await helper.find_in_channel(member.id)
	info=await helper.find_in_info(member.id)
	await inter.respond(
		embed=discord.Embed(
			title="Profile Menu!",
			description=data[2],
			color=discord.Color.from_rgb(213, 240, 213),
			timestamp=datetime.datetime.utcnow()
				).set_author(
					name=f"{member.name} (@{data[1]})",
					icon_url=data[3]
				).set_footer(
					text=f"Source: @{data[1]} | ID: {member.id}",
					icon_url=data[3]
				).add_field(
					name="Subs",
					value=data[4]
				).add_field(
					name="Videos",
					value=data[8]
				).add_field(
					name="Views",
					value=data[7]
				).add_field(
					name="Likes",
					value=data[5]
				).add_field(
					name="Dislikes",
					value=data[6]
				).add_field(
					name="\u200b",
					value="\u200b"
				).add_field(
					name="Account Information",
					value="Here is all of your account information! You can change it using p!set command!",
					inline=False
				).add_field(
					name="Gender",
					value=info[1]
				).add_field(
					name="Email",
					value=info[3]
				).add_field(
					name="Password",
					value="||Shushh||",
					inline=False
				).add_field(
					name="Account Age",
					value=info[5]
				)
			)


@slash.message_command(name="Resend", guild_ids=guild_ids)
async def resend(inter):
    # Message commands are visible in message context menus
    # inter is instance of ContextMenuInteraction
    await inter.respond(inter.message.content)

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
		
	emojies={"Owner": "👑", "Fun": "🤡", "Social": "🗨️", "Jishaku": "⚙️", "Information": "🛑"}

	num_commands={"Owner": "4", "Fun": "2", "Social": "6", "Jishaku": "1", "Information": "2"}

	em=discord.Embed(
		title="HelpCommand",
		description="Hello there, im Tango. A fun bot with a social media functions! Gain followers, million of views, and become the most followed channel! Post your meme and messages in community post! Post your video and get ton of review! All seen across multiple country!\n\n**Select A Category:**",
		color=discord.Color.orange()
	)
	
	for x in categories:
		em.add_field(
			name=f"{emojies[x]} {x} [{num_commands[x]}]",
			value=cog_description[x],
			inline=False
		)

	await inter.reply(embed=em)