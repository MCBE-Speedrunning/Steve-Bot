from discord.ext import commands
from discord.ext import tasks
from discord.utils import get
import discord
import requests
import json
import asyncio
from datetime import timedelta
from google.cloud import translate_v2 as translate
translate_client = translate.Client()

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


async def verifyRole(self, ctx, apiKey):
	server = self.bot.get_guild(574267523869179904)
	RunneRole = server.get_role(574268937454223361)
	WrRole = server.get_role(583622436378116107)
	head = {
		"X-API-Key":apiKey,
		"Accept": "application/json",
		"User-Agent":"mcbeDiscordBot/1.0"
		}
	r = requests.get('https://www.speedrun.com/api/v1/profile', headers=head)

	#print(profile.text)
	profile = json.loads(r.text)
	pbs = requests.get(profile["data"]["links"][3]["uri"])
	pbs = json.loads(pbs.text)

	for i in pbs["data"]:
		if i["place"] == 1:
			if i["run"]["game"] == "yd4ovvg1" or i["run"]["game"] == "v1po7r76":
				await ctx.send("WR boi")
				await server.get_member(ctx.message.author.id).add_roles(WrRole)
				print("WR boi")
		if i["run"]["game"] == "yd4ovvg1" or i["run"]["game"] == "v1po7r76":
			#print(i)
			await ctx.send("Runner")
			await server.get_member(ctx.message.author.id).add_roles(RunneRole)
			#print("minecraft")

	print(r.status_code)
	#print(json.dumps(pbs,sort_keys=True, indent=4))

async def clear(self):
	async for msg in self.bot.get_channel(699713639866957905).history():
		await msg.delete()


async def pendingRuns(self, ctx):
	head = {
		"Accept": "application/json",
		"User-Agent":"mcbeDiscordBot/1.0"
		}
	# mgs = [] #Empty list to put all the messages in the log
	# number = int(number) #Converting the amount of messages to delete to an integer
	# async for x in Client.logs_from(ctx.message.channel, limit = number):
	#	 mgs.append(x)
	# await Client.delete_messages(mgs)

	gameID = 'yd4ovvg1'  # ID of Minecraft bedrock
	gameID2 = 'v1po7r76'  # ID of Category extension
	runsRequest = requests.get(
		f'https://www.speedrun.com/api/v1/runs?game={gameID}&status=new&max=200', headers=head)
	runs = json.loads(runsRequest.text)
	runsRequest2 = requests.get(
		f'https://www.speedrun.com/api/v1/runs?game={gameID2}&status=new&max=200', headers=head)
	runs2 = json.loads(runsRequest2.text)
	# Use https://www.speedrun.com/api/v1/games?abbreviation=mcbe for ID

	for game in range(2):
		for i in range(200):
			try:
				for key, value in runs['data'][i].items():
					if key == 'weblink':
						link = value
					if key == 'category':
						categoryID = value
						categoryRequest = requests.get(
							f"https://www.speedrun.com/api/v1/categories/{categoryID}", headers=head)
						categoryRequest = categoryRequest.json()
						categoryName = categoryRequest['data']['name']
					if key == 'players':
						if value[0]['rel'] == 'guest':
							player = value[0]['name']
						else:
							nameRequest = requests.get(value[0]['uri'])
							nameRequest = nameRequest.json()
							player = nameRequest['data']['names']['international']
					if key == 'times':
						rta = timedelta(seconds=value['realtime_t'])
			except Exception as e:
				#print(e.message + '\n' + e.args)
				break
			if game == 0:
				leaderboard = "Minecraft bedrock"
			elif game == 1:
				leaderboard = "Minecraft Bedrock category extensions"
			embed = discord.Embed(
				title=leaderboard, url=link, description=f"{categoryName} in `{str(rta).replace('000','')}` by **{player}**", color=16711680+i*60)
			await self.bot.get_channel(699713639866957905).send(embed=embed)
		runs = runs2
		gameID = gameID2

class Utils(commands.Cog):

	def __init__(self, bot):
		self.bot = bot

	@commands.command()
	async def ping(self, ctx):
		# """Shows the Client Latency."""
		await ctx.send(f'Pong! {round(self.bot.latency*1000)}ms')

	@commands.command()
	async def test(self, ctx):
		await ctx.send(ctx.message.channel)

	@commands.command()
	async def pending(self, ctx):
		await clear(self)
		await pendingRuns(self, ctx)

	@commands.command()
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
	
	@commands.command()
	async def verify(self, ctx, apiKey=None):
		if apiKey is None:
			await ctx.send("Please try this `/verify apiKey` again **in DMs**. If you need the api key you can get it from https://www.speedrun.com/api/auth")
		if ctx.guild is None:
			await verifyRole(self, ctx, apiKey)
		else:
			await ctx.message.delete()
			print("Not DMs")

def setup(bot):
	bot.add_cog(Utils(bot))
