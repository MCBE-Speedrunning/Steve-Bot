from discord.ext import commands
import discord
import asyncio
import logging
from random import randint

class Welcome(commands.Cog):
    # Welcome message + set roles when new member joined
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_join(self, member):
        server = member.guild
        welcome_channel = self.bot.get_channel(740051039499059271)
        # TODO: find a way to get channel id if possible
        member_role = discord.utils.get(member.guild.roles, name="Member")
        welcome_msg=[f"It's a Bird, It's a Plane, It's {member.mention}!",
                f"Welcome {member.mention}! <:PogChamp:740102448047194152>",
                f"Good to see you, {member.mention}."]
        await member.add_roles(member_role)
        await welcome_channel.send(f"{welcome_msg[randint(0, len(welcome_msg) - 1)]}")

def setup(bot):
    bot.add_cog(Welcome(bot))
