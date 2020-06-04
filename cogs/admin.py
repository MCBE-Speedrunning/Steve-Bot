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
	
	@commands.Cog.listener()
	async def on_deleted_message(message):
		channel = self.bot.get_channel(718187032869994686)
		embed = discord.Embed(
			title = f'Deleted Message by {message.author}',
			description = 'message.content',
			color = message.author.color,
			timestamp = message.created_at
		)
		await channel.send(embed)

	@commands.command(aliases=['deleteEverything'], hidden=True)
	@commands.check(is_mod)
	async def purge(self, ctx, password):
		if password == "MaxCantBeTrusted":
			async for msg in ctx.channel.history():
				await msg.delete()

	@commands.command(aliases=['quit'], hidden=True)
	@commands.check(is_mod)
	async def forceexit(self, ctx, password):
		if password == "abort":
			ctx.message.delete()
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
			json.dump(self.bot.custom_commands, f)

		await ctx.send(f"Set message for command {command}")

	@commands.command(aliases=['deletecommand'])
	@commands.check(is_mod)
	async def removecommand(self, ctx, command):
		del self.bot.custom_commands[ctx.prefix + command]
		with open('custom_commands.json', 'w') as f:
			json.dump(self.bot.custom_commands, f)

		await ctx.send(f"Removed command {command}")
			
	
	@commands.check(is_mod)
	@commands.command(name='reload', hidden=True, usage='<extension>')
	async def _reload(self, ctx, ext):
		"""Reloads an extension"""
		try:
			self.bot.reload_extension(f'cogs.{ext}')
			await ctx.send(f'The extension {ext} was realoaded!') # Oceanlight told me too
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
			self.bot.logger.exception(f'Failed to reload extension {ext}:')

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
	async def mute(self, ctx, members: commands.Greedy[discord.Member],
					   mute_minutes: int = 0,
					   *, reason: str = "absolutely no reason"):
		"""Mass mute members with an optional mute_minutes parameter to time it"""

		if not members:
			await ctx.send("You need to name someone to mute")
			return

		#muted_role = discord.utils.find(ctx.guild.roles, name="Muted")
		muted_role = ctx.guild.get_role(707707894694412371)
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
		muted_role = ctx.guild.get_role(707707894694412371)
		for i in members:
			await i.remove_roles(muted_role)
			await ctx.send("{0.mention} has been unmuted by {1.mention}".format(i, ctx.author))

	@commands.command()
	@commands.check(is_mod)
	async def logs(self, ctx, *, password):
		if password == "beep boop":
			await ctx.message.delete()
			file = discord.File("discord.log")
			await ctx.send(file=file)



def setup(bot):
	bot.add_cog(Admin(bot))
