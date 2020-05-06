from discord.ext import commands
import discord
import logging

import datetime
import config
import json

extensions = [
    "cogs.utils",
    "cogs.admin"
]

class BedrockBot(commands.Bot):

    def __init__(self):
        super().__init__(command_prefix='/')
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

        command = message.content.split()[0] 

        if command in self.custom_commands:
            await message.channel.send(self.custom_commands[command])
            return

        badWords = ["fair", "f a i r", "ⓕⓐⓘⓡ", "ⓕ ⓐ ⓘ ⓡ"]
        if message.channel.id == 589110766578434078:
            count = 0
            for word in badWords:
                if word in message.content.lower():
                    count += 1;
                    await message.channel.send('Fair '*count)

        await self.process_commands(message)

    def run(self):
        super().run(config.token, reconnect=True)
