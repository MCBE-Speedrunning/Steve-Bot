import asyncio
import datetime
import functools
import json
from datetime import timedelta
# forgot to import this and ended up looking mentally unstable
# troll literally pointed out atleast 4 things I did wrong in 3 lines of code
from random import choice, randint

import discord
from discord.ext import commands, tasks
#from PIL.Image import core as Image
#import image as Image
from PIL import Image, ImageFilter
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


def set_viewport_size(driver, width, height):
	window_size = driver.execute_script("""
		return [window.outerWidth - window.innerWidth + arguments[0],
		  window.outerHeight - window.innerHeight + arguments[1]];
		""", width, height)
	driver.set_window_size(*window_size)

async def reportStuff(self, ctx, message):
	channel = self.bot.get_channel(int(self.bot.config[str(ctx.message.guild.id)]["report_channel"]))

	embed = discord.Embed(
				title=f"Report from {ctx.message.author}",
				description=f"{message}",
				color=ctx.message.author.color, timestamp=ctx.message.created_at)

	await channel.send(embed=embed)
	await ctx.author.send("Report has been submitted")

def save_leaderboard():
	DRIVER = '/usr/lib/chromium-browser/chromedriver'
	chrome_options = Options()
	chrome_options.add_argument("--disable-dev-shm-usage")
	chrome_options.add_argument("--headless")
	chrome_options.add_argument("--no-sandbox")
	chrome_options.add_argument("--disable-gpu")
	#chrome_options.binary_location = ""
	driver = webdriver.Chrome(DRIVER, chrome_options=chrome_options)
	set_viewport_size(driver, 1000, 1000)
	driver.get('https://aninternettroll.github.io/mcbeVerifierLeaderboard/')
	screenshot = driver.find_element_by_id('table').screenshot('leaderboard.png')
	driver.quit()
	#transparency time
	img = Image.open('leaderboard.png')
	img = img.convert("RGB")
	pallette = Image.open("palette.png")
	pallette = pallette.convert("P")
	img = img.quantize(colors=256, method=3, kmeans=0, palette=pallette)
	img = img.convert("RGBA")
	datas = img.getdata()

	newData = []
	for item in datas:
		if item[0] == 255 and item[1] == 255 and item[2] == 255:
			newData.append((255, 255, 255, 0))
		else:
			newData.append(item)

	img.putdata(newData)
	"""
	img = img.filter(ImageFilter.SHARPEN)
	img = img.filter(ImageFilter.SHARPEN)
	img = img.filter(ImageFilter.SHARPEN)
	"""
	#height, width = img.size
	#img = img.resize((height*10,width*10), resample=Image.BOX)
	img.save("leaderboard.png", "PNG")

class Utils(commands.Cog):

	def __init__(self, bot):
		self.bot = bot
		self.tries = 1

	@commands.command(description="Pong!", help="Tells the ping of the bot to the discord servers", brief="Tells the ping")
	async def ping(self, ctx):
		await ctx.send(f'Pong! {round(self.bot.latency*1000)}ms')

	@commands.cooldown(1, 25, commands.BucketType.guild)
	@commands.command()
	async def findseed(self, ctx):
		"""Test your luck"""
		if ctx.message.channel.id != int(self.bot.config[str(ctx.message.guild.id)]["bot_channel"]):
			await ctx.message.delete()
			ctx.command.reset_cooldown(ctx)
			return

		# Don't ask
		rigged_findseed = {
			280428276810383370: 12,	 # Thomas's User ID
			199070670221475842: -1,	 # Kai's User ID
			615658069132836865: -12	 # What a fraud! They didn't use their real name.
		}

		if ctx.author.id in rigged_findseed:
			totalEyes = rigged_findseed[ctx.author.id]
		else:
			totalEyes = 0
			for i in range(12):
				randomness = randint(1, 10)
				if randomness <= 1:
					totalEyes += 1
		await ctx.send(f"{discord.utils.escape_mentions(ctx.message.author.display_name)} -> your seed is a {totalEyes} eye")

	@findseed.error
	async def findseed_handler(self,ctx,error):
		if isinstance(error, commands.CommandOnCooldown):
			if ctx.message.channel.id != int(self.bot.config[str(ctx.message.guild.id)]["bot_channel"]):
				ctx.command.reset_cooldown(ctx)
				await ctx.message.delete()
				return
		else:
			await ctx.send(error)
			#await ctx.send(f"{discord.utils.escape_mentions(ctx.message.author.display_name)}, you have to wait {round(error.retry_after, 7)} seconds before using this again.")

	@commands.command()
	async def findsleep(self, ctx):
		"""Test your sleep"""
		if ctx.message.channel.id != int(self.bot.config[str(ctx.message.guild.id)]["bot_channel"]):
			await ctx.message.delete()
			return

		# DON'T ASK!
		lessSleepMsg = [
			"gn, insomniac!",
			"counting sheep didn't work? try counting chloroform vials!",
			"try a glass of water",
			"some decaf coffee might do the trick!"
		]

		moreSleepMsg = [
			"waaakeee uuuppp!",
			"are they dead or asleep? I can't tell.",
			"wake up, muffin head",
			"psst... coffeeee \\:D"
		]

		# Optional TODO: Create non-normal distribution
		sleepHrs = randint(0, 24)

		# Add extra comment based on number of sleepHrs
		if sleepHrs == 0:
						await ctx.send(f"{discord.utils.escape_mentions(ctx.message.author.display_name)} -> your sleep is 0 hours long - nice try \:D")
		elif sleepHrs <= 5:
			if sleepHrs == 1:
				s = ''
			else:
				s = 's'
			await ctx.send(f"{discord.utils.escape_mentions(ctx.message.author.display_name)} -> your sleep is {sleepHrs} hour{s} long - {lessSleepMsg[randint(0, len(lessSleepMsg) - 1)]}")
		else:
			await ctx.send(f"{discord.utils.escape_mentions(ctx.message.author.display_name)} -> your sleep is {sleepHrs} hours long - {moreSleepMsg[randint(0, len(moreSleepMsg) - 1)]}")

	@commands.Cog.listener()
	async def on_member_join(self, member):
		if member.id == 640933433215811634:
			await member.edit(nick="JoetheSheepFucker")
		def check(msg):
			return msg.author == member and msg.type != discord.MessageType.new_member
		try:
			msg = await self.bot.wait_for("message", check=check, timeout=300)
			await msg.channel.send("<:PeepoPog:732172337956257872>")
		except asyncio.TimeoutError:
			await msg.channel.send("<:pepesadcrash:739927552260440185>")
	
	@commands.Cog.listener()
	async def on_member_update(self, before, after):
		if after.id == 640933433215811634:
			await after.edit(nick="JoetheSheepFucker")

	@commands.Cog.listener()
	async def on_message(self, message):
		if not message.guild:
			return
		if message.channel.id != int(self.bot.config[str(message.guild.id)]["fair_channel"]):
			return
		if message.author.bot:
			return
		badWords = ["fair", "ⓕⓐⓘⓡ"]
		count = 0

		coolKids = [
			['Cameron', self.bot.get_user(468262902969663488), datetime.date(2020, 10, 8)],
			['Indy', self.bot.get_user(274923326890311691), datetime.date(2020, 9, 10)],
			['Kai', self.bot.get_user(199070670221475842), datetime.date(2020, 11, 20)],
			['Luca', self.bot.get_user(99457716614885376), datetime.date(2020, 11, 5)],
			['Max', self.bot.get_user(543958509243596800), datetime.date(2020, 11, 10)],
			['Mistaken', self.bot.get_user(264121998173536256), datetime.date(2020, 7, 6)],
			['Murray', self.bot.get_user(400344183333847060), datetime.date(2020, 11, 10)],
			['RKREE', self.bot.get_user(395872198323077121), datetime.date(2020, 11, 5)],
			# idk if she goes by her irl name but I'm sticking with it for the sake of uniformity
			# also idk how to pronounce prakxo
			['Samantha', self.bot.get_user(226312219787264000), datetime.date(2020, 6, 24)],
			['Scott', self.bot.get_user(223937483774230528), datetime.date(2020, 6, 23)],
			['Sky', self.bot.get_user(329538915805691905), datetime.date(2020, 6, 24)],
			['Thomas', self.bot.get_user(280428276810383370), datetime.date(2020, 9, 29)],
			['Zyemlus', self.bot.get_user(536071288859656193), datetime.date(2020, 8, 23)],
			['Landen', self.bot.get_user(654025117025828885), datetime.date(2020, 8, 25)],
			['Oceanlight', self.bot.get_user(615658069132836865), datetime.date(2020, 4, 9)]
		]


		for coolKid in coolKids:
			if datetime.date.today() == coolKid[2]:
				try:
					for i in range(self.tries):
						await coolKid[1].send(f'Happy Birthday {coolKid[0]}! You\'re a boomer now! :mango:')
					self.tries = 1
				except:
					self.tries +=1

		for word in badWords:
			if word in message.content.lower().replace(" ", ""):
				count += 1;
				fair = 'Fair '*count
		await message.channel.send(fair)

	@commands.cooldown(1, 60, commands.BucketType.member)
	@commands.command()
	async def report(self, ctx, *, message=None):
		"""Send a message to the super mods about anything"""
		if ctx.message.guild != None:
			await ctx.message.delete()
		if message == None:
			await ctx.message.author.send("Please type a report to report (hehe, sounds funny)")
		else:
			await reportStuff(self, ctx, message)

	@commands.cooldown(1, 20, commands.BucketType.guild)
	@commands.command()
	async def leaderboard(self, ctx):
		"""Leaderboard of the people that matter"""
		async with ctx.typing():
			try:
				lbFunc = functools.partial(save_leaderboard)
				await self.bot.loop.run_in_executor(None, lbFunc)
				await ctx.send(file=discord.File("leaderboard.png"))
			except:
				await ctx.send("https://aninternettroll.github.io/mcbeVerifierLeaderboard/")

	@leaderboard.error
	async def leaderboard_handler(self,ctx,error):
		if isinstance(error, commands.CommandOnCooldown):
			#return
			await ctx.send(f"{discord.utils.escape_mentions(ctx.message.author.display_name)}, you have to wait {round(error.retry_after, 2)} seconds before using this again.")

	@commands.cooldown(1, 60, commands.BucketType.guild)
	@commands.command()
	async def someone(self, ctx):
		"""Discord's mistake"""
		if ctx.channel.id != int(self.bot.config[str(ctx.message.guild.id)]["fair_channel"]):
			await ctx.send(choice(ctx.guild.members).mention)

	@commands.command()
	async def roll(self, ctx, pool):
		"""Roll the dice"""
		await ctx.send(f"You rolled a {randint(0, int(pool))}")

	@commands.command(aliases=['commands', 'allcommands'])
	async def listcommands(self, ctx):
		"""List all custom commands"""
		with open('custom_commands.json', 'r') as f:
			commands = json.load(f)
			output = ", ".join([*commands])
			await ctx.send(f"```List of custom commands:\n{output}```")

def setup(bot):
	bot.add_cog(Utils(bot))
