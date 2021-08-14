import discord

from dislash import ActionRow, Button, ButtonStyle, SelectMenu, SelectOption
from discord.ext import commands

class Information(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

	@commands.command("idea", description="SHow a list of ideas for Tango bot in the future")
	async def _idea(self, ctx):
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
		msg=await ctx.send(
			embed=discord.Embed(
				title="Tango Bot",
				url="https://discord.com/api/oauth2/authorize?client_id=806725119917162527&permissions=242933428048&scope=applications.commands%20bot",
				description=f"Hello {ctx.author.mention}, im Tango! A discord bot with Social Media Functions. Gain followers, Post your favorite video and get tons of views! Become the most followed channel! Post your meme and messages in community post! Interact with your fans through community post! All seen across multiple country! \n\n([invite me!](https://discord.com/api/oauth2/authorize?client_id=806725119917162527&permissions=242933428048&scope=applications.commands%20bot) | [Support Server](https://discord.gg/XHBhg6A4jJ))",
				color=discord.Color.from_rgb(213, 240, 213)
			),
			components=[
				ActionRow(
					Button(
						style=ButtonStyle.grey,
						label="Commands",
						emoji="\U00002699",
						custom_id="command-button"
						
					),
					Button(
						style=ButtonStyle.grey,
						label="Database",
						emoji="\U0001f3e6",
						custom_id="database-button"
						
					),
					Button(
						style=ButtonStyle.grey,
						label="Tango",
						emoji="\U0001f916",
						custom_id="robot-button"
					)
				)
			]
		)
		owner=self.bot.get_user(685082846993317953)
		while True:
			inter=await ctx.wait_for_button_click(lambda inter: inter.author == ctx.author and inter.channel == ctx.channel)
			id_=inter.clicked_button.custom_id
			if id_ == "command-button":
				await msg.edit(
					embed=discord.Embed(
						title="Tango Bot",
						url="https://discord.com/api/oauth2/authorize?client_id=806725119917162527&permissions=242933428048&scope=applications.commands%20bot",
						description=f"Hello {ctx.author.mention}, im Tango! A discord bot with Social Media Functions. Gain followers, Post your favorite video and get tons of views! Become the most followed channel! Post your meme and messages in community post! Interact with your fans through community post! All seen across multiple country! \n\n([invite me!](https://discord.com/api/oauth2/authorize?client_id=806725119917162527&permissions=242933428048&scope=applications.commands%20bot) | [Support Server](https://discord.gg/XHBhg6A4jJ))",
						color=discord.Color.from_rgb(213, 240, 213)
					),
					components=[
						ActionRow(
							Button(
								style=ButtonStyle.grey,
								label="Commands",
								emoji="\U00002699",
								custom_id="command-button",
								disabled=True
							),
							Button(
								style=ButtonStyle.grey,
								label="Database",
								emoji="\U0001f3e6",
								custom_id="database-button"
							),
							Button(
								style=ButtonStyle.grey,
								label="Tango",
								emoji="\U0001f916",
								custom_id="robot-button"
							)
						)
					]
				)
				await inter.send(
					embed=discord.Embed(
						title="Commands",
						url="https://discord.com/api/oauth2/authorize?client_id=806725119917162527&permissions=242933428048&scope=applications.commands%20bot",
						description="Tango bot have a lot of command categories, right now Tango bot has 4 categories, 15 commands, 10 of them can be use by anyone without any special permissions!",
						color=discord.Color.from_rgb(213, 240, 213)
					),
					ephemeral=True
				)

			elif id_ == "database-button":
				await msg.edit(
					embed=discord.Embed(
						title="Tango Bot",
						url="https://discord.com/api/oauth2/authorize?client_id=806725119917162527&permissions=242933428048&scope=applications.commands%20bot",
						description=f"Hello {ctx.author.mention}, im Tango! A discord bot with Social Media Functions. Gain followers, Post your favorite video and get tons of views! Become the most followed channel! Post your meme and messages in community post! Interact with your fans through community post! All seen across multiple country! \n\n([invite me!](https://discord.com/api/oauth2/authorize?client_id=806725119917162527&permissions=242933428048&scope=applications.commands%20bot) | [Support Server](https://discord.gg/XHBhg6A4jJ))",
						color=discord.Color.from_rgb(213, 240, 213)
					),
					components=[
						ActionRow(
							Button(
								style=ButtonStyle.grey,
								label="Commands",
								emoji="\U00002699",
								custom_id="command-button"
							),
							Button(
								style=ButtonStyle.grey,
								label="Database",
								emoji="\U0001f3e6",
								custom_id="database-button",
								disabled=True
								
							),
							Button(
								style=ButtonStyle.grey,
								label="Tango",
								emoji="\U0001f916",
								custom_id="robot-button"
							)
						)
					]
				)
				await inter.send(
					embed=discord.Embed(
						title="Database",
						url="https://www.sqlite.org/index.html",
						description="Tango use sqlite type database specifically Tango bot uses aiosqlite. Dont you worry, The data will not be delete and it will not be reset. The data also hold a lot of capacity!",
						color=discord.Color.from_rgb(213, 240, 213)
					),
					ephemeral=True
				)
			
			elif id_ == "robot-button":
				await msg.edit(
					embed=discord.Embed(
						title="Tango Bot",
						url="https://discord.com/api/oauth2/authorize?client_id=806725119917162527&permissions=242933428048&scope=applications.commands%20bot",
						description=f"Hello {ctx.author.mention}, im Tango! A discord bot with Social Media Functions. Gain followers, Post your favorite video and get tons of views! Become the most followed channel! Post your meme and messages in community post! Interact with your fans through community post! All seen across multiple country! \n\n([invite me!](https://discord.com/api/oauth2/authorize?client_id=806725119917162527&permissions=242933428048&scope=applications.commands%20bot) | [Support Server](https://discord.gg/XHBhg6A4jJ))",
						color=discord.Color.from_rgb(213, 240, 213)
					),
					components=[
						ActionRow(
							Button(
								style=ButtonStyle.grey,
								label="Commands",
								emoji="\U00002699",
								custom_id="command-button"
							),
							Button(
								style=ButtonStyle.grey,
								label="Database",
								emoji="\U0001f3e6",
								custom_id="database-button"
								
							),
							Button(
								style=ButtonStyle.grey,
								label="Tango",
								emoji="\U0001f916",
								custom_id="robot-button",
								disabled=True
							)
						)
					]
				)
				
				await inter.send(
					embed=discord.Embed(
						title="Tango Bot",
						url="https://discord.com/api/oauth2/authorize?client_id=806725119917162527&permissions=242933428048&scope=applications.commands%20bot",
						description=f"Tango was created by {owner.name} at the 4th of February 2021 as an AutoRoleBot. TheGenocide change the idea to SocialMedia bot after a while of thinking and its rare to find SocialMedia bot.",
						color=discord.Color.from_rgb(213, 240, 213)
					),
					ephemeral=True
				)

			

def setup(bot):
	bot.add_cog(Information(bot))