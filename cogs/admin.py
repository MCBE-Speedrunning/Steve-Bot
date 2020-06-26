from discord.ext import commands
import discord
import asyncio
import subprocess
import json
import git
import os

class Admin(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

	async def is_mod(ctx):
		return ctx.author.guild_permissions.manage_channels

	async def is_botmaster(ctx):
		return ctx.author.id in ctx.bot.config[str(ctx.message.guild.id)]["bot_masters"]

	@commands.command(aliases=['deleteEverything'], hidden=True)
	async def purge(self, ctx):
		if ctx.author.id in self.bot.config[str(ctx.message.guild.id)]["bot_masters"]:
			async for msg in ctx.channel.history():
				await msg.delete()

	@commands.command(aliases=['quit'], hidden=True)
	async def forceexit(self, ctx):
		if ctx.author.id in self.bot.config[str(ctx.message.guild.id)]["bot_masters"]:
			await ctx.send('Self Destructing')
			exit()

	@commands.command()
	@commands.check(is_mod)
	async def pull(self, ctx):
		g = git.cmd.Git(os.getcwd())
		await ctx.send(f"Probably pulled.\n```bash\n{g.pull()}```")

	@commands.command(aliases=['addcommand', 'newcommand'])
	@commands.check(is_mod)
	async def setcommand(self, ctx, command, *, message):
		self.bot.custom_commands[ctx.prefix + command] = message
		with open('custom_commands.json', 'w') as f:
			json.dump(self.bot.custom_commands, f, indent=4)

		await ctx.send(f"Set message for command {command}")

	@commands.command(aliases=['deletecommand'])
	@commands.check(is_mod)
	async def removecommand(self, ctx, command):
		del self.bot.custom_commands[ctx.prefix + command]
		with open('custom_commands.json', 'w') as f:
			json.dump(self.bot.custom_commands, f, indent=4)

		await ctx.send(f"Removed command {command}")

	@commands.check(is_mod)
	@commands.command(name='reload', hidden=True, usage='<extension>')
	async def _reload(self, ctx, ext):
		"""Reloads an extension"""
		try:
			self.bot.reload_extension(f'cogs.{ext}')
			await ctx.send(f'The extension {ext} was reloaded!')
		except commands.ExtensionNotFound:
			await ctx.send(f'The extension {ext} doesn\'t exist.')
		except commands.ExtensionNotLoaded:
			await ctx.send(f'The extension {ext} is not loaded! (use {ctx.prefix}load)')
		except commands.NoEntryPointError:
			await ctx.send(f'The extension {ext} doesn\'t have an entry point (try adding the setup function) ')
		except commands.ExtensionFailed:
			await ctx.send(f'Some unknown error happened while trying to reload extension {ext} (check logs)')
			self.bot.logger.exception(f'Failed to reload extension {ext}:')

	@commands.check(is_mod)
	@commands.command(name='load', hidden=True, usage='<extension>')
	async def _load(self, ctx, ext):
		"""Loads an extension"""
		try:
			self.bot.load_extension(f'cogs.{ext}')
			await ctx.send(f'The extension {ext} was loaded!')
		except commands.ExtensionNotFound:
			await ctx.send(f'The extension {ext} doesn\'t exist!')
		except commands.ExtensionAlreadyLoaded:
			await ctx.send(f'The extension {ext} is already loaded.')
		except commands.NoEntryPointError:
			await ctx.send(f'The extension {ext} doesn\'t have an entry point (try adding the setup function)')
		except commands.ExtensionFailed:
			await ctx.send(f'Some unknown error happened while trying to reload extension {ext} (check logs)')
			self.bot.logger.exception(f'Failed to reload extension {ext}:')

	@commands.check(is_mod)
	@commands.command(name='unload', hidden=True, usage='<extension>')
	async def _unload(self, ctx, ext):
		"""Loads an extension"""
		try:
			self.bot.unload_extension(f'cogs.{ext}')
			await ctx.send(f'The extension {ext} was unloaded!')
		except commands.ExtensionNotFound:
			await ctx.send(f'The extension {ext} doesn\'t exist!')
		except commands.NoEntryPointError:
			await ctx.send(f'The extension {ext} doesn\'t have an entry point (try adding the setup function)')
		except commands.ExtensionFailed:
			await ctx.send(f'Some unknown error happened while trying to reload extension {ext} (check logs)')
			self.bot.logger.exception(f'Failed to unload extension {ext}:')

	"""
	@commands.command()
	@commands.check(is_mod)
	async def connect(self, ctx):
		await ctx.author.voice.channel.connect()
		await ctx.send(f"Joined channel {ctx.author.voice.channel.name}")

	@commands.command()
	@commands.check(is_mod)
	async def disconnect(self, ctx):
		await ctx.voice_client.disconnect()
		await ctx.send(f"Left channel {ctx.author.voice.channel.name}")
	"""

	@commands.command()
	@commands.check(is_mod)
	async def clear(self, ctx, number):
		await ctx.message.channel.purge(limit=int(number)+1, check=None, before=None, after=None, around=None, oldest_first=False, bulk=True)

	@commands.check(is_mod)
	@commands.command()
	async def mute(self, ctx, members: commands.Greedy[discord.Member]=False,
					   mute_minutes: int = 0,
					   *, reason: str = "absolutely no reason"):
		"""Mass mute members with an optional mute_minutes parameter to time it"""

		if not members:
			await ctx.send("You need to name someone to mute")
			return
		elif type(members)==str:
			members = [self.bot.get_user(int(members))]

		#muted_role = discord.utils.find(ctx.guild.roles, name="Muted")
		muted_role = ctx.guild.get_role(int(self.bot.config[str(ctx.message.guild.id)]["mute_role"]))
		for member in members:
			if self.bot.user == member: # what good is a muted bot?
				embed = discord.Embed(title = "You can't mute me, I'm an almighty bot")
				await ctx.send(embed = embed)
				continue
			await member.add_roles(muted_role, reason = reason)
			await ctx.send("{0.mention} has been muted by {1.mention} for *{2}*".format(member, ctx.author, reason))

		if mute_minutes > 0:
			await asyncio.sleep(mute_minutes * 60)
			for member in members:
				await member.remove_roles(muted_role, reason = "time's up ")

	@commands.check(is_mod)
	@commands.command()
	async def unmute(self, ctx, members: commands.Greedy[discord.Member]):
		if not members:
			await ctx.send("You need to name someone to unmute")
			return
		elif type(members)==str:
			members = self.bot.get_user(int(user))

		muted_role = ctx.guild.get_role(int(self.bot.config[str(ctx.message.guild.id)]["mute_role"]))
		for i in members:
			await i.remove_roles(muted_role)
			await ctx.send("{0.mention} has been unmuted by {1.mention}".format(i, ctx.author))

	@commands.command()
	@commands.check(is_botmaster)
	async def logs(self, ctx, *):
		await ctx.message.delete()
		file = discord.File("discord.log")
		await ctx.send(file=file)

	@commands.command(aliases=['ban'], hidden=True)
	@commands.check(is_mod)
	async def blacklist(self, ctx, members: commands.Greedy[discord.Member]=None):
		if not members:
			await ctx.send("You need to name someone to blacklist")
			return
		elif type(members)=="str":
			members = self.bot.get_user(int(user))

		with open('blacklist.json', 'w') as f:
			for i in members:
				if i.id in self.bot.blacklist:
					self.bot.blacklist.remove(i.id)
					json.dump(self.bot.blacklist, f, indent=4)
					await ctx.send(f"{i} has been un-blacklisted.")
				else:
					self.bot.blacklist.append(i.id)
					json.dump(self.bot.blacklist, f, indent=4)
					await ctx.send(f"{i} has been blacklisted.")

	@commands.command()
	@commands.check(is_mod)
	async def activity(self, ctx, *, activity=None):
		if activity:
			game = discord.Game(activity)
		else:
			activity = "Mining away"
			game = discord.Game(activity)
		await self.bot.change_presence(activity=game)
		await ctx.send(f"Activity changed to {activity}")

	@commands.command()
	async def setvar(self, ctx, key, *, value):
		if ctx.author.id in self.bot.config[str(ctx.message.guild.id)]["bot_masters"]:
			with open('config.json', 'w') as f:
				if value[0] == '[' and value[len(value)-1] == ']':
					value = list(map(int, value[1:-1].split(',')))
				self.bot.config[str(ctx.message.guild.id)][key] = value
				json.dump(self.bot.config, f, indent=4)

	@commands.command()
	@commands.check(is_mod)
	async def printvar(self, ctx, key):
		await ctx.send(self.bot.config[str(ctx.message.guild.id)][key])


def setup(bot):
	bot.add_cog(Admin(bot))
