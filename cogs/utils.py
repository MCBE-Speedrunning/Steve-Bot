from discord.ext import commands
from discord.ext import tasks
import discord
import requests
import json
import asyncio
from datetime import timedelta

async def reportStuff(self, ctx, message):
	channel = self.bot.get_channel(715549209998262322)

	embed = discord.Embed(
				title=f"Report from {ctx.message.author.mention}",
				description=f"{message}", 
				color=16711680, timestamp=ctx.message.created_at)

	await channel.send(embed=embed)
	await ctx.send("Report has been submitted")

class Utils(commands.Cog):

	def __init__(self, bot):
		self.bot = bot

	@commands.command(description="Pong!", help="Tells the ping of the bot to the discord servers", brief="Tells the ping")
	async def ping(self, ctx):
		await ctx.send(f'Pong! {round(self.bot.latency*1000)}ms')

	@commands.cooldown(1, 25, commands.BucketType.guild)
	@commands.command()
	async def findseed(self, ctx):
		if ctx.message.channel.id != 684787316489060422:
			ctx.message.delete()
			return
		totalEyes = 0
		for i in range(12):
			randomness = random.randint(1,10)
			if randomness == 1:
				totalEyes += randomness
			else:
				continue
		await ctx.send(f"{ctx.message.author.display_name} -> your seed is a {totalEyes} eye")

	@findseed.error
	async def findseed_handler(self,ctx,error):
		if isinstance(error, commands.CommandOnCooldown):
			if ctx.message.channel.id != 684787316489060422:
				ctx.message.delete()
			return
			#await ctx.send(f"{ctx.message.author.display_name}, you have to wait {round(error.retry_after, 7)} seconds before using this again.")

	@commands.Cog.listener()
	async def on_message(self, message):
		if message.channel.id != 589110766578434078:
			return
		if message.author.bot:
			return
		badWords = ["fair", "f a i r", "ⓕⓐⓘⓡ", "ⓕ ⓐ ⓘ ⓡ"]
		count = 0
		for word in badWords:
			if word in message.content.lower():
				count += 1;
				fair = 'Fair '*count
		await message.channel.send(fair)

	@commands.cooldown(1, 60, commands.BucketType.member)
	@commands.command()
	async def report(self, ctx, *, message=None):
		if message == None:
			await ctx.send("Please type a report to report (hehe, sounds funny)")
		else:
			await reportStuff(self, ctx, message)

def setup(bot):
	bot.add_cog(Utils(bot))
