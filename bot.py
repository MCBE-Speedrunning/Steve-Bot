from discord.ext import commands
import discord
import logging

import datetime
import config
import json

extensions = [
	"cogs.utils",
	"cogs.admin",
	"cogs.src",
	"cogs.help"
]
def get_prefix(bot, message):
	"""A callable Prefix for our bot. This could be edited to allow per server prefixes."""

	prefixes = ['/', '!', 'steve ']

	# Check to see if we are outside of a guild. e.g DM's etc.
	#if not message.guild:
		# Only allow ? to be used in DMs
	#	return '?'

	# If we are in a guild, we allow for the user to mention us or use any of the prefixes in our list.
	return commands.when_mentioned_or(*prefixes)(bot, message)

class BedrockBot(commands.Bot):

	def __init__(self):
		super().__init__(command_prefix=get_prefix)
		self.logger = logging.getLogger('discord')

		with open('custom_commands.json', 'r') as f:
			self.custom_commands = json.load(f)

		for extension in extensions:
			self.load_extension(extension)

	async def on_ready(self):
		self.uptime = datetime.datetime.utcnow()

		game = discord.Game("Mining away")
		await self.change_presence(activity=game)

		self.logger.warning(f'Online: {self.user} (ID: {self.user.id})')

	async def on_message(self, message):

		if message.author.bot:
			return
		await self.process_commands(message)

		command = message.content.split()[0] 

		if command in self.custom_commands:
			await message.channel.send(self.custom_commands[command])
			return

	def run(self):
		super().run(config.token, reconnect=True)
