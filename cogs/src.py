from discord.ext import commands
from discord.ext import tasks
from discord.utils import get
import discord
import requests
import json
import asyncio
from datetime import timedelta

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
	gameID = 'yd4ovvg1'  # ID of Minecraft bedrock
	gameID2 = 'v1po7r76'  # ID of Category extension
	runsRequest = requests.get(
		f'https://www.speedrun.com/api/v1/runs?game={gameID}&status=new&max=200&embed=category,players', headers=head)
	runs = json.loads(runsRequest.text)
	runsRequest2 = requests.get(
		f'https://www.speedrun.com/api/v1/runs?game={gameID2}&status=new&max=200&embed=category,players', headers=head)
	runs2 = json.loads(runsRequest2.text)
	# Use https://www.speedrun.com/api/v1/games?abbreviation=mcbe for ID

	for game in range(2):
		for i in range(200):
			try:
				for key, value in runs['data'][i].items():
					if key == 'weblink':
						link = value
					if key == 'category':
						categoryName = value["data"]["name"]
					if key == 'players':
						if value["data"][0]['rel'] == 'guest':
							player = value["data"][0]['name']
						else:
							player = value["data"][0]["names"]["international"]
					if key == 'times':
						rta = timedelta(seconds=value['realtime_t'])
			except Exception as e:
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

class Src(commands.Cog):

	def __init__(self, bot):
		self.bot = bot

	@commands.command(description="Posts all pending runs to #pending-runs")
	@commands.guild_only()
	async def pending(self, ctx):
		await clear(self)
		await pendingRuns(self, ctx)

	@commands.command()
	async def verify(self, ctx, apiKey=None):
		if apiKey == None:
			await ctx.send(f"Please try again this command by getting an apiKey from https://www.speedrun.com/api/auth then do `{ctx.prefix}verify <apiKey>` in my DMs or anywhere in this server. \nBe careful who you share this key with. To learn more check out https://github.com/speedruncomorg/api/blob/master/authentication.md")
			return
		elif ctx.guild != None:
			await ctx.message.delete()
		await verifyRole(self, ctx, apiKey)

def setup(bot):
	bot.add_cog(Src(bot))