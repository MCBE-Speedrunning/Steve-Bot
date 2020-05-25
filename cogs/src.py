from discord.ext import commands
from discord.ext import tasks
from discord.utils import get
import discord
import requests
import json
import asyncio
from datetime import timedelta

async def rejectRun(self, apiKey, ctx, run, reason):
	await ctx.message.delete()
	run = run.split('/')[-1]
	reject = {
		"status": {
		"status": "rejected",
		"reason": reason
		}
	}
	r = requests.put(f"https://www.speedrun.com/api/v1/runs/{run}/status", headers={"X-API-Key":apiKey,	"Accept": "application/json","User-Agent":"mcbeDiscordBot/1.0"}, data=json.dumps(reject))
	if r.status_code == 200 or r.status_code == 204:
		await ctx.send("Run rejected succesfully")
	else:
		await ctx.send("Something went wrong")
		await ctx.message.author.send(f"```json\n{json.dumps(json.loads(r.text),indent=4)}```")

async def approveRun(self, apiKey, ctx, run, reason=None):
	await ctx.message.delete()
	run = run.split('/')[-1]
	approve = {
		"status": {
		"status": "verified",
		"reason": reason
		}
	}
	r = requests.put(f"https://www.speedrun.com/api/v1/runs/{run}/status", headers={"X-API-Key":apiKey,	"Accept": "application/json","User-Agent":"mcbeDiscordBot/1.0"}, data=json.dumps(approve))
	if r.status_code == 200 or r.status_code == 204:
		await ctx.send("Run approved succesfully")
	else:
		await ctx.send("Something went wrong")
		await ctx.message.author.send(f"```json\n{json.dumps(json.loads(r.text),indent=4)}```")

async def deleteRun(self, apiKey, ctx, run):
	await ctx.message.delete()
	run = run.split('/')[-1]
	r = requests.delete(f"https://www.speedrun.com/api/v1/runs/{run}", headers={"X-API-Key":apiKey,"Accept": "application/json","User-Agent":"mcbeDiscordBot/1.0"})
	if r.status_code == 200 or r.status_code == 204:
		await ctx.send("Run deleted succesfully")
	else:
		await ctx.send("Something went wrong")
		await ctx.message.author.send(f"```json\n{json.dumps(json.loads(r.text),indent=4)}```")


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
				if not i["run"]["level"]:
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
	mcbe_runs = 0
	mcbeil_runs = 0
	mcbece_runs = 0
	head = {
		"Accept": "application/json",
		"User-Agent":"mcbeDiscordBot/1.0"
		}
	gameID = 'yd4ovvg1'  # ID of Minecraft bedrock
	gameID2 = 'v1po7r76'  # ID of Category extension
	runsRequest = requests.get(
		f'https://www.speedrun.com/api/v1/runs?game={gameID}&status=new&max=200&embed=category,players,level&orderby=submitted', headers=head)
	runs = json.loads(runsRequest.text)
	runsRequest2 = requests.get(
		f'https://www.speedrun.com/api/v1/runs?game={gameID2}&status=new&max=200&embed=category,players,level&orderby=submitted', headers=head)
	runs2 = json.loads(runsRequest2.text)
	# Use https://www.speedrun.com/api/v1/games?abbreviation=mcbe for ID

	for game in range(2):
		for i in range(200):
			leaderboard = '' # A little ugly but prevents name not defined error
			level = False
			try:
				for key, value in runs['data'][i].items():
					if key == 'weblink':
						link = value
					if key == 'level':
						if value["data"]:
							level = True
							leaderboard = 'Individual Level Run'
							categoryName = value["data"]["name"]
							mcbeil_runs += 1
						else:
							mcbe_runs += 1
					if key == 'category' and not level:
						categoryName = value["data"]["name"]
					if key == 'players':
						if value["data"][0]['rel'] == 'guest':
							player = value["data"][0]['name']
						else:
							player = value["data"][0]["names"]["international"]
					if key == 'times':
						rta = timedelta(seconds=value['realtime_t'])
			except Exception as e:
				print(e.args)
				break
			if game == 0 and leaderboard != 'Individual Level Run':
				leaderboard = "Full Game Run"
			elif game == 1 and leaderboard != 'Individual Level Run':
				leaderboard = "Category Extension Run"
				mcbece_runs += 1
			embed = discord.Embed(
				title=leaderboard, url=link, description=f"{categoryName} in `{str(rta).replace('000','')}` by **{player}**", color=16711680+i*60)
			await self.bot.get_channel(699713639866957905).send(embed=embed)
		runs = runs2
		gameID = gameID2
	embed_stats = discord.Embed(title='Pending Run Stats', description=f"Full Game Runs: {mcbe_runs}\nIndividual Level Runs: {mcbeil_runs}\nCategory Extension Runs: {mcbece_runs}", color=16711680 + i * 60)
	await self.bot.get_channel(699713639866957905).send(embed=embed_stats)

class Src(commands.Cog):

	def __init__(self, bot):
		self.bot = bot

	async def is_mod(ctx):
		return ctx.author.guild_permissions.manage_channels

	@commands.command(description="Posts all pending runs to #pending-runs")
	@commands.guild_only()
	async def pending(self, ctx):
		async with ctx.typing():
			await clear(self)
			await pendingRuns(self, ctx)

	@commands.command()
	async def verify(self, ctx, apiKey=None):
		if apiKey == None:
			await ctx.send(f"Please try again this command by getting an apiKey from https://www.speedrun.com/api/auth then do `{ctx.prefix}verify <apiKey>` in my DMs or anywhere in this server. \nBe careful who you share this key with. To learn more check out https://github.com/speedruncomorg/api/blob/master/authentication.md")
			return
		elif ctx.guild != None:
			await ctx.message.delete()
		async with ctx.typing():
			await verifyRole(self, ctx, apiKey)

	@commands.command(description="Reject runs quickly")
	@commands.check(is_mod)
	@commands.guild_only()
	async def reject(self, ctx, apiKey, run, *, reason):
		await rejectRun(self, apiKey, ctx, run, reason)

	@commands.command(description="Approve runs quickly")
	@commands.check(is_mod)
	@commands.guild_only()
	async def approve(self, ctx, apiKey, run, *, reason=None):
		await approveRun(self, apiKey, ctx, run, reason)

	@commands.command(description="Delete runs quickly")
	@commands.check(is_mod)
	@commands.guild_only()
	async def delete(self, ctx, apiKey, run):
		await deleteRun(self, apiKey, ctx, run)

def setup(bot):
	bot.add_cog(Src(bot))
