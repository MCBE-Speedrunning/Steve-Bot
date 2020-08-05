from discord.ext import commands
import discord
import asyncio
import logging

class Welcome(commands.Cog):
    # Welcome message + set roles when new member joined
    def __init__(self, bot):
        self.bot = bot
        self.logger = logging.getLogger('discord')

    @commands.Cog.listener()
    async def on_member_join(self, member):
        server = member.guild
        welcome_channel = self.bot.get_channel(740051039499059271)
        member_role = discord.utils.get(member.guild.roles, name="Member")
        await member.add_roles(member_role)
        self.logger.info(f'New member: {member.name} (ID: {member.id})'
        await welcome_channel.send(f"Welcome {member.mention}, to {server.name}! <:PogChamp:740102448047194152>")

    @commands.command(aliases=['test'])
    async def _test(self, ctx):
        welcome_channel = self.bot.get_channel(740051039499059271)
        await welcome_channel.send("test")

def setup(bot):
    bot.add_cog(Welcome(bot))
