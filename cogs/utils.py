from discord.ext import commands
from discord.ext import tasks
import discord
import requests
import json
import asyncio
from datetime import timedelta
from google.cloud import translate_v2 as translate
translate_client = translate.Client()
import random

async def translateMsg(text, target="en"):
	# Text can also be a sequence of strings, in which case this method
	# will return a sequence of results for each text.
	result = translate_client.translate(
		text, target_language=target)
	print(u'Text: {}'.format(result['input']))
	print(u'Translation: {}'.format(result['translatedText']))
	print(u'Detected source language: {}'.format(
		result['detectedSourceLanguage']))
	return result;

class Utils(commands.Cog):

	def __init__(self, bot):
		self.bot = bot

	@commands.command(description="Pong!", help="Tells the ping of the bot to the discord servers", brief="Tells the ping")
	async def ping(self, ctx):
		await ctx.send(f'Pong! {round(self.bot.latency*1000)}ms')

	@commands.command(help="Translate text in english (using google translate)", brief="Translate to english")
	async def translate(self, ctx, *, message):
		response = await translateMsg(message)
		embed=discord.Embed(title="Translation",description=f"{ctx.message.author.mention} says:", timestamp=ctx.message.created_at, color=0x4d9aff)
		embed.add_field(name=f"[{response['detectedSourceLanguage']}] Source:" , value=response['input'], inline=False)
		embed.add_field(name="Translation", value=response['translatedText'], inline=True)
		await ctx.send(embed=embed)

	@commands.command()
	async def trans(self, ctx, lan, *, message):
		response = await translateMsg(message, lan)
		embed=discord.Embed(title="Translation",description=f"{ctx.message.author.mention} says:", timestamp=ctx.message.created_at, color=0x4d9aff)
		embed.add_field(name=f"[{response['detectedSourceLanguage']}] Source:" , value=response['input'], inline=False)
		embed.add_field(name="Translation", value=response['translatedText'], inline=True)
		await ctx.send(embed=embed)

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

def setup(bot):
	bot.add_cog(Utils(bot))
