from discord.ext import commands
import discord
import json
import aiohttp
import logging

extensions = [
	"cogs.moderator", "cogs.general", "cogs.welcome", "cogs.util"
]

def get_prefix(bot, message):
	"""A callable Prefix for our bot. This could be edited to allow per server prefixes."""

	prefixes = ['/', '!', '+', '.']

	# Check to see if we are outside of a guild. e.g DM's etc.
	# if not message.guild:
	# Only allow ? to be used in DMs
	#   return '?'

	# If we are in a guild, we allow for the user to mention us or use any of the prefixes in our list.
	return commands.when_mentioned_or(*prefixes)(bot, message)

class ziBot(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix=get_prefix,case_insensitive=True)

        self.logger = logging.getLogger('discord')
        self.session = aiohttp.ClientSession()
        
        with open('config.json', 'r') as f:
            self.config = json.load(f)
            config = self.config

    async def on_ready(self): 
        activity=discord.Activity(name="some test",type=discord.ActivityType.watching)
        await self.change_presence(activity=activity)

        for extension in extensions:
            self.load_extension(extension)
        
        self.logger.warning(f'Online: {self.user} (ID: {self.user.id})')
        print(f'Online: {self.user} (ID: {self.user.id})') 

    async def on_message(self, message):
        await self.process_commands(message)
        try:
            command = message.content.split()[0]
        except IndexError:
            pass
        print('Message from {0.author}: {0.content} on {0.channel}'.format(message))

    def run(self):
        super().run(self.config["token"], reconnect=True)
