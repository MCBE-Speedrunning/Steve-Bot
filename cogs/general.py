from discord.ext import commands
import discord
import asyncio

class General(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=['add'])
    async def _add(self, ctx):
        oauth_link = "https://discord.com/oauth2/authorize?client_id=740122842988937286&scope=bot"
        await ctx.send(f"To add ziBot to your server, click here: \n {oauth_link}")
    
    @commands.command(aliases=['source'])
    async def sauce(self, ctx):
        git_link = "<PutLinkHere>"
        await ctx.send(f"ziBot's Source Code: \n {git_link}")

def setup(bot):
    bot.add_cog(General(bot))

