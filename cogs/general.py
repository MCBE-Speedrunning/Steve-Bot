from discord.ext import commands
import discord
import asyncio

class General(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def add(self, ctx):
        oauth_link = "https://discord.com/oauth2/authorize?client_id=740122842988937286&scope=bot"
        await ctx.send(f"To add ziBot to your server, click here: \n {oauth_link}")
    
    @commands.command()
    async def source(self, ctx):
        git_link = "https://github.com/null2264/ziBot"
        await ctx.send(f"ziBot's Source Code: \n {git_link}")

def setup(bot):
    bot.add_cog(General(bot))

