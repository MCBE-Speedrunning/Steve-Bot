from discord.ext import commands
import discord
import asyncio

class General(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def add(self, ctx):
        """Show link to invite ziBot."""
        oauth_link = "https://discord.com/oauth2/authorize?client_id=740122842988937286&scope=bot"
        await ctx.send(f"To add ziBot to your server, click here: \n {oauth_link}")
    
    @commands.command()
    async def source(self, ctx):
        """Show link to ziBot's source code."""
        git_link = "https://github.com/null2264/ziBot"
        await ctx.send(f"ziBot's source code: \n {git_link}")

    @commands.command()
    async def serverinfo(self, ctx):
        """Show server information"""
        embed = discord.Embed(
                title=f"{ctx.guild.name} Information",
                colour=discord.Colour.orange()
                )
        # embed.set_author(name=f"{ctx.guild.name} Information")
        embed.set_thumbnail(url=ctx.guild.icon_url)
        _emoji=""
        member_count=len(ctx.guild.members)
        embed.add_field(name="Members",value=f"{member_count}")
        for emoji in ctx.guild.emojis:
            _emoji+= ", ".join([f"{str(emoji)}"])
        embed.add_field(name="Emojis",value=f"{_emoji}")
        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(General(bot))

