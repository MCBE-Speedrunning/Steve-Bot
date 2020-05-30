from discord.ext import commands
from discord.ext import tasks
from discord.utils import get
from datetime import timedelta
import discord
import requests
import json
import asyncio
import dateutil.parser
from pathlib import Path

async def rejectRun(self, apiKey, ctx, run, reason):
	await ctx.message.delete()
	run = run.split('/')[-1]
	reject = {
		"status": {
			"status": "rejected",
			"reason": reason
		}
	}
	r = requests.put(f"https://www.speedrun.com/api/v1/runs/{run}/status", headers={
					 "X-API-Key": apiKey, "Accept": "application/json", "User-Agent": "mcbeDiscordBot/1.0"}, data=json.dumps(reject))
	if r.status_code == 200 or r.status_code == 204:
		await ctx.send("Run rejected succesfully")
	else:
		await ctx.send("Something went wrong")
		await ctx.message.author.send(f"```json\n{json.dumps(json.loads(r.text),indent=4)}```")


async def approveRun(self, apiKey, ctx, run, reason=None):
	await ctx.message.delete()
	run = run.split('/')[-1]
	if reason == None:
		approve = {
			"status": {
				"status": "verified"
			}
		}
	else:
		approve = {
			"status": {
				"status": "verified",
				"reason":reason
			}
		}
	r = requests.put(f"https://www.speedrun.com/api/v1/runs/{run}/status", headers={
					 "X-API-Key": apiKey, "Accept": "application/json", "User-Agent": "mcbeDiscordBot/1.0"}, data=json.dumps(approve))
	if r.status_code == 200 or r.status_code == 204:
		await ctx.send("Run approved succesfully")
	else:
		await ctx.send("Something went wrong")
		await ctx.message.author.send(f"```json\n{json.dumps(json.loads(r.text),indent=4)}```")


async def deleteRun(self, apiKey, ctx, run):
	await ctx.message.delete()
	run = run.split('/')[-1]
	r = requests.delete(f"https://www.speedrun.com/api/v1/runs/{run}", headers={
						"X-API-Key": apiKey, "Accept": "application/json", "User-Agent": "mcbeDiscordBot/1.0"})
	if r.status_code == 200 or r.status_code == 204:
		await ctx.send("Run deleted succesfully")
	else:
		await ctx.send("Something went wrong")
		await ctx.message.author.send(f"```json\n{json.dumps(json.loads(r.text),indent=4)}```")

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
							categoryName = value["data"]["name"]
					if key == 'category' and not level:
						categoryName = value["data"]["name"]
					if key == 'players':
						if value["data"][0]['rel'] == 'guest':
							player = value["data"][0]['name']
						else:
							player = value["data"][0]["names"]["international"]
					if key == 'times':
						rta = timedelta(seconds=value['realtime_t'])
					if key == 'submitted':
						timestamp = dateutil.parser.isoparse(value)
			except Exception as e:
				print(e.args)
				break
			if game == 0:
				if level == True:
					mcbeil_runs += 1
					leaderboard = 'Individual Level Run'
				else:
					mcbe_runs += 1
					leaderboard = "Full Game Run" # If this doesn't work I'm starting a genocide
			elif game == 1:
				leaderboard = "Category Extension Run"
				mcbece_runs += 1
			embed = discord.Embed(
				title=leaderboard, url=link, description=f"{categoryName} in `{str(rta).replace('000','')}` by **{player}**", color=16711680+i*60, timestamp=timestamp)
			await self.bot.get_channel(699713639866957905).send(embed=embed)
		runs = runs2
		gameID = gameID2
	embed_stats = discord.Embed(title='Pending Run Stats', description=f"Full Game Runs: {mcbe_runs}\nIndividual Level Runs: {mcbeil_runs}\nCategory Extension Runs: {mcbece_runs}", color=16711680 + i * 60)
	await self.bot.get_channel(699713639866957905).send(embed=embed_stats)


async def verifyNew(self, apiKey=None, userID=None):
	if apiKey==None:
		head = {
		"Accept": "application/json",
		"User-Agent": "mcbeDiscordBot/1.0"
		}
	else:
		head = {
		"X-API-Key": apiKey,
		"Accept": "application/json",
		"User-Agent": "mcbeDiscordBot/1.0"
		}
	server = self.bot.get_guild(574267523869179904)
	# Troll is mentally challenged I guess ¯\_(ツ)_/¯
	RunneRole = server.get_role(574268937454223361)
	WrRole = server.get_role(583622436378116107)
	#if userID == None:
	#	return
	#else:
	user = self.bot.get_user(int(userID))
	data = json.loads(Path('./api_keys.json').read_text())

	if str(user.id) in data:
		pbs = requests.get(f"https://www.speedrun.com/api/v1/users/{data[str(user.id)]}/personal-bests", headers=head)
		pbs = json.loads(pbs.text)
	else:
		r = requests.get(
			'https://www.speedrun.com/api/v1/profile', headers=head)
		# print(r.text)
		if r.status_code >= 400:
			await user.send(f"```json\n{r.text}```")
			return
		try:
			profile = json.loads(r.text)
		except json.decoder.JSONDecodeError:
			return
		srcUserID = profile["data"]["id"]
		with open('api_keys.json', 'w') as file:
			data[user.id] = srcUserID
			json.dump(data, file, indent=4)
		pbs = requests.get(profile["data"]["links"][3]["uri"], headers=head)
		pbs = json.loads(pbs.text)

	for i in pbs["data"]:
		if i["place"] == 1:
			if i["run"]["game"] == "yd4ovvg1" or i["run"]["game"] == "v1po7r76":
				if not i["run"]["level"]:
					await server.get_member(user.id).add_roles(WrRole)
		if i["run"]["game"] == "yd4ovvg1" or i["run"]["game"] == "v1po7r76":
			# I have no shame
			await server.get_member(user.id).add_roles(RunneRole)

class Src(commands.Cog):

	def __init__(self, bot):
		self.bot = bot
		self.checker.start()

	async def is_mod(ctx):
		return ctx.author.guild_permissions.manage_channels

	@commands.command(description="Posts all pending runs to #pending-runs")
	@commands.guild_only()
	async def pending(self, ctx):
		async with ctx.typing():
			await clear(self)
			await pendingRuns(self, ctx)

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

	@commands.command()
	async def verify(self, ctx, apiKey=None, userID=None):
		#if apiKey == None:
		#	await ctx.send(f"Please try again this command by getting an apiKey from https://www.speedrun.com/api/auth then do `{ctx.prefix}verify <apiKey>` in my DMs or anywhere in this server. \nBe careful who you share this key with. To learn more check out https://github.com/speedruncomorg/api/blob/master/authentication.md")
		#	return
		if ctx.guild != None:
			await ctx.message.delete()
		async with ctx.typing():
			if userID == None:
				userID = ctx.message.author.id
			await verifyNew(self, apiKey, userID)

	@tasks.loop(minutes=2.0)
	async def checker(self):
		data = json.loads(Path('./api_keys.json').read_text())
		for key,value in data.items():
			await verifyNew(self, None, key)


def setup(bot):
	bot.add_cog(Src(bot))
