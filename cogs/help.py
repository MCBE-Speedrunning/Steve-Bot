from discord.ext import commands
import discord
import asyncio

class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def help(self, ctx):
        """Show this message."""
        embed = discord.Embed(
                    title = "Help",
                    description = f"*` Bot prefixes are '>' and '$>' `*",
                    colour = discord.Colour.green()
                )

        cmds = list(self.bot.commands)
        for cmd in cmds:
            if cmd.hidden is True:
                continue
            if cmd.help is None:
                _desc="No description."
            else:
                _desc=f"{cmd.help}"
            _cmd = f"{str(cmd)}"
            embed.add_field(name=f"{_cmd}", value=f"{_desc}", inline=False)

        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(Help(bot))

