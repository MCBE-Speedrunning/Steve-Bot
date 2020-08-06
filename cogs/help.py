from discord.ext import commands
import discord
import asyncio
import json

class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=["commands"])
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
            _cmd = " | ".join([str(cmd),*cmd.aliases])
            embed.add_field(name=f"{_cmd}", value=f"{_desc}", inline=False)

        await ctx.send(embed=embed)

    @commands.command(aliases=['customcommands', 'ccmds'])
    async def listcommands(self, ctx):
        """List all custom commands"""
        embed = discord.Embed(
                    title = "Help",
                    colour = discord.Colour.gold()
                )
        with open('custom_commands.json', 'r') as f:
            commands = json.load(f)
            ccmds = ", ".join([*commands])
            # await ctx.send(f"```List of custom commands: \n{ccmds}```")
            # output += f'{ccmds}```'
        embed.add_field(name="Custom Commands", value=f"{ccmds}", inline=False)
        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(Help(bot))

