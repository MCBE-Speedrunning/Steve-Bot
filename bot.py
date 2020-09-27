import datetime
import json
import logging

import aiohttp
import discord
from discord.ext import commands

extensions = [
    "cogs.utils",
    "cogs.admin",
    "cogs.src",
    "cogs.trans",
    "cogs.player",
    "cogs.general",
    # "cogs.webserver",
    # "cogs.twitter",
    "cogs.logs",
    "cogs.errorhandler",
]


def get_prefix(bot, message):
    """A callable Prefix for our bot. This could be edited to allow per server prefixes."""

    prefixes = ["steve ", "STEVE ", "/", "!", "@", "Steve "]

    # Check to see if we are outside of a guild. e.g DM's etc.
    # if not message.guild:
    # Only allow ? to be used in DMs
    #   return '?'

    # If we are in a guild, we allow for the user to mention us or use any of the prefixes in our list.
    return commands.when_mentioned_or(*prefixes)(bot, message)


class BedrockBot(commands.Bot):
    def __init__(self):
        super().__init__(
            command_prefix=get_prefix,
            case_insensitive=True,
            allowed_mentions=discord.AllowedMentions(
                everyone=False, users=True, roles=False
            ),
        )
        self.logger = logging.getLogger("discord")
        self.messageBlacklist = []
        self.session = aiohttp.ClientSession()

        with open("custom_commands.json", "r") as f:
            self.custom_commands = json.load(f)

        with open("config.json", "r") as f:
            self.config = json.load(f)
            config = self.config

    async def on_ready(self):
        self.uptime = datetime.datetime.utcnow()

        game = discord.Game("Mining away")
        await self.change_presence(activity=game)

        with open("blacklist.json", "r") as f:
            try:
                self.blacklist = json.load(f)
            except json.decoder.JSONDecodeError:
                self.blacklist = []

        with open("runs_blacklist.json", "r") as f:
            try:
                self.runs_blacklist = json.load(f)
            except json.decoder.JSONDecodeError:
                self.runs_blacklist = {"videos": [], "players": []}

        for extension in extensions:
            self.load_extension(extension)

        self.logger.warning(f"Online: {self.user} (ID: {self.user.id})")

    async def on_message(self, message):

        if message.author.bot or message.author.id in self.blacklist:
            return
        await self.process_commands(message)

        try:
            command = message.content.split()[0]
        except IndexError:
            pass
        try:
            if command in self.custom_commands:
                await message.channel.send(self.custom_commands[command])
                return
        except:
            return

    def run(self):
        super().run(self.config["token"], reconnect=True)
