from discord.ext import commands
import discord
import asyncio

class Welcome(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_join(self, member):
        server = member.guild
        welcome_channel = self.bot.get_channel(740051039499059271)
        await welcome_channel.send(f"Welcome {member.mention}, to {server.name}! <:PogChamp:740102448047194152>")

    @commands.command(aliases=['test'])
    async def _test(self, ctx):
        welcome_channel = self.bot.get_channel(740051039499059271)
        await welcome_channel.send("test")

def setup(bot):
    bot.add_cog(Welcome(bot))