from discord.ext import commands
from discord.ext import tasks
import discord
import requests
import json
import asyncio
import datetime
# forgot to import this and ended up looking mentally unstable
# troll literally pointed out atleast 4 things I did wrong in 3 lines of code
from random import choice
from random import randint
from datetime import timedelta
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
#from PIL.Image import core as Image
#import image as Image
from PIL import Image
from PIL import ImageFilter

def set_viewport_size(driver, width, height):
	window_size = driver.execute_script("""
		return [window.outerWidth - window.innerWidth + arguments[0],
		  window.outerHeight - window.innerHeight + arguments[1]];
		""", width, height)
	driver.set_window_size(*window_size)

async def reportStuff(self, ctx, message):
	channel = self.bot.get_channel(715549209998262322)

	embed = discord.Embed(
				title=f"Report from {ctx.message.author}",
				description=f"{message}", 
				color=ctx.message.author.color, timestamp=ctx.message.created_at)

	await channel.send(embed=embed)
	await ctx.author.send("Report has been submitted")

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
		if ctx.message.channel.id != 684787316489060422:
			await ctx.message.delete()
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
			
		await ctx.send(f"{ctx.message.author.display_name} -> your seed is a {totalEyes} eye")

	@findseed.error
	async def findseed_handler(self,ctx,error):
		if isinstance(error, commands.CommandOnCooldown):
			if ctx.message.channel.id != 684787316489060422:
				await ctx.message.delete()
				return
		else:
			await ctx.send(error)
			#await ctx.send(f"{ctx.message.author.display_name}, you have to wait {round(error.retry_after, 7)} seconds before using this again.")

	@commands.command()
	async def findsleep(self, ctx):
		if ctx.message.channel.id != 684787316489060422:
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
			"psst... coffeeee \:D"
		]
	
		# Set up initial message
		msg = f"{ctx.message.author.display_name} -> "

		# Optional TODO: Create non-normal distribution
		sleepHrs = randint(0, 24)

		# Add sleepHrs with bonus grammar check :D
		if sleepHrs == 1:
			msg += f"your sleep is {sleepHrs} hour long "
		else:
			msg += f"your sleep is {sleepHrs} hours long "

		# Add extra comment based on number of sleepHrs
		if sleepHrs == 0:
			msg += "- nice try \:D"
		elif sleepHrs <= 5:
			msg += f"- {lessSleepMsg[randint(0, len(lessSleepMsg) - 1)]}"
		elif sleepHrs >= 10:
			msg += f"- {moreSleepMsg[randint(0, len(moreSleepMsg) - 1)]}"
			
		await ctx.send(msg)

	@commands.Cog.listener()
	async def on_message(self, message):
		if message.channel.id != 589110766578434078:
			return
		if message.author.bot:
			return
		badWords = ["fair", "f a i r", "ⓕⓐⓘⓡ", "ⓕ ⓐ ⓘ ⓡ"]
		count = 0
		
		coolKids = [
			['Cameron', self.bot.get_user(468262902969663488), datetime.date(2020, 10, 8)],
			['Indy', self.bot.get_user(274923326890311691), datetime.date(2020, 9, 10)],
			['Kai', self.bot.get_user(199070670221475842), datetime.date(2020, 11, 20)],
			['Luca', self.bot.get_user(99457716614885376), datetime.date(2020, 11, 5)],
			['Max', self.bot.get_user(543958509243596800), datetime.date(2020, 11, 10)],
			['Murray', self.bot.get_user(400344183333847060), datetime.date(2020, 11, 10)],
			# idk if she goes by her irl name but I'm sticking with it for the sake of uniformity
			# also idk how to pronounce prakxo
			['Samantha', self.bot.get_user(226312219787264000), datetime.date(2020, 6, 25)],
			['Scott', self.bot.get_user(223937483774230528), datetime.date(2020, 6, 23)],
			['Thomas', self.bot.get_user(280428276810383370), datetime.date(2020, 9, 29)]
		]
		
		
		# Luca plz dont remove the bottom code (just incase the new code doesnt work,
		# and also for me to laugh at how bad my code is)
		
		# brb while I write ugly and inefficient code in my
		# conquest to make Steve the Bot bloated and unworkable
		
		#if datetime.date.today() == datetime.date(2020, 6, 23):
		#	await scott.send('Happy Birthday Scott. You\'re a boomer now! :mango:')
		#elif datetime.date.today() == datetime.date(2020, 6, 25):
		#	await samantha.send('Happy Birthday Prakxo. You\'re a boomer now! :mango:')
		#elif datetime.date.today() == datetime.date(2020, 5, 28):
		#	await thomas.send('Testy Test :mango:')
		#elif datetime.date.today() == datetime.date(2020, 9, 29):
		#	await thomas.send('Now you know how the others felt :mango:')
		#elif datetime.date.today() == datetime.date(2020, 10, 8):
		#	await cameron.send('Happy Birthday Cameron. You\'re a boomer now! :mango:')
		#elif datetime.date.today() == datetime.date(2020, 11, 10):
		#	await murray.send('Happy Birthday Murray. You\'re a boomer now! :mango:')
		#elif datetime.date.today() == datetime.date(2020, 9, 10):
		#	await indy.send('Happy Birthday Indy. You\'re a boomer now! :mango:)
		
		# Ignore the above message. I got sick and tired of looking at trash code
		
		for coolKid in coolKids:
			if datetime.date.today() == coolKid[2]:
				try:
					for i in range(self.tries):
						await coolKid[1].send(f'Happy Birthday {coolKid[0]}! You\'re a boomer now! :mango:')
					self.tries = 1
				except:
					self.tries +=1
			
		for word in badWords:
			if word in message.content.lower():
				count += 1;
				fair = 'Fair '*count
		await message.channel.send(fair)

	@commands.cooldown(1, 60, commands.BucketType.member)
	@commands.command()
	async def report(self, ctx, *, message=None):
		if ctx.message.guild != None:
			await ctx.message.delete()
		if message == None:
			await ctx.message.author.send("Please type a report to report (hehe, sounds funny)")
		else:
			await reportStuff(self, ctx, message)

	@commands.cooldown(1, 20, commands.BucketType.member)
	@commands.command()
	async def leaderboard(self, ctx):
		async with ctx.typing():
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

			await ctx.send(file=discord.File("leaderboard.png"))


	@leaderboard.error
	async def leaderboard_handler(self,ctx,error):
		if isinstance(error, commands.CommandOnCooldown):
			#return
			await ctx.send(f"{ctx.message.author.display_name}, you have to wait {round(error.retry_after, 2)} seconds before using this again.")
	
	# Why? Because I can. lel
	
	# celeste guyToday at 6:13 PM
	# @Mango Man that's not how it works
	
	# Mango ManToday at 6:13 PM
	# it looks fine in lightmode
	# wait whats not how what works
	
	# celeste guyToday at 6:13 PM
	# the command
	
	# Mango ManToday at 6:13 PM
	# o
	# how does it work
	
	# celeste guyToday at 6:14 PM
	# Like for a start, nothing is defined
	# use ctx D:
	
	# Mango ManToday at 6:14 PM
	# Do I need to though?
	
	# celeste guyToday at 6:14 PM
	# ctx.guild.members() or something
	# Yes, server is not a thing
	# 2nd, mention is not used like that
	# You still have to send a message
	# And mention in the message
	
	# Mango ManToday at 6:14 PM
	# o
	
	# celeste guyToday at 6:15 PM
	# 3rd, don't forget to import choice from random
	
	# Mango ManToday at 6:15 PM
	# this is why you dont steal code from github
	# I actually feel embarrased over forgetting to import random
	
	# celeste guyToday at 6:15 PM
	# 4th, add ctx in the arguments list, or you'll get an error like "function takes 1 argument but 2 were given"
	# And you will use it to send the message and get the server
	# Also forgetting the import is the least embarrassing thing
	# Since I did remove it
	# And replaced with import randint from random
	
	@commands.command()
	async def someone(self, ctx):
				blacklist = [536071288859656193]
				if ctx.channel.id != 589110766578434078:
						if ctx.author.id == 395872198323077121:
								await ctx.send("grape is a bitch")
						elif ctx.author.id == 521153476714299402:
								await ctx.send("ZMG is smooth brain")
						elif ctx.author.id == 199070670221475842:
								await ctx.send(f"fuck you {ctx.message.author.mention}")
						elif ctx.author.id in blacklist:
								await ctx.send("not even bothering with a message for you. You're just an edgy sheep")
						else:
								await ctx.send(choice(ctx.guild.members).mention)

	@commands.command()
	async def roll(self, ctx, pool):
		await ctx.send(f"You rolled a {randint(0, int(pool))}")

	@commands.command(aliases=['commands', 'allcommands'])
	async def listcommands(self, ctx):
		with open('custom_commands.json', 'r') as f:
			commands = json.load(f)
			output = '```List of custom commands:\n'
			for key in commands:
				output += f'{key}, '
			output += '```'
			await ctx.send(output)

def setup(bot):
	bot.add_cog(Utils(bot))
