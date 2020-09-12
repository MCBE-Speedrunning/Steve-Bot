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
# from PIL.Image import core as Image
# import image as Image
from PIL import Image, ImageFilter
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


def set_viewport_size(driver, width, height):
    window_size = driver.execute_script(
        """
		return [window.outerWidth - window.innerWidth + arguments[0],
		  window.outerHeight - window.innerHeight + arguments[1]];
		""",
        width,
        height,
    )
    driver.set_window_size(*window_size)


async def reportStuff(self, ctx, message):
    channel = self.bot.get_channel(
        int(self.bot.config[str(ctx.message.guild.id)]["report_channel"])
    )

    embed = discord.Embed(
        title=f"Report from {ctx.message.author}",
        description=f"{message}",
        color=ctx.message.author.color,
        timestamp=ctx.message.created_at,
    )

    await channel.send(embed=embed)
    await ctx.author.send("Report has been submitted")


def save_leaderboard():
    DRIVER = "/usr/lib/chromium-browser/chromedriver"
    chrome_options = Options()
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-gpu")
    # chrome_options.binary_location = ""
    driver = webdriver.Chrome(DRIVER, chrome_options=chrome_options)
    set_viewport_size(driver, 1000, 1000)
    driver.get("https://aninternettroll.github.io/mcbeVerifierLeaderboard/")
    screenshot = driver.find_element_by_id("table").screenshot("leaderboard.png")
    driver.quit()
    # transparency time
    img = Image.open("leaderboard.png")
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
    # height, width = img.size
    # img = img.resize((height*10,width*10), resample=Image.BOX)
    img.save("leaderboard.png", "PNG")


class Utils(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.tries = 1
        self.pins = []

    @commands.command(
        description="Pong!",
        help="Tells the ping of the bot to the discord servers",
        brief="Tells the ping",
    )
    async def ping(self, ctx):
        await ctx.send(f"Pong! {round(self.bot.latency*1000)}ms")

    @commands.cooldown(1, 25, commands.BucketType.guild)
    @commands.command()
    async def findseed(self, ctx):
        """Test your luck"""
        if ctx.message.channel.id != int(
            self.bot.config[str(ctx.message.guild.id)]["bot_channel"]
        ):
            await ctx.message.delete()
            ctx.command.reset_cooldown(ctx)
            return

        # Don't ask
        rigged_findseed = {
            280428276810383370: 12,  # Thomas's User ID
            199070670221475842: -1,  # Kai's User ID
            615658069132836865: -12,  # What a fraud! They didn't use their real name.
        }

        if ctx.author.id in rigged_findseed:
            total_eyes = rigged_findseed[ctx.author.id]
        else:
            total_eyes = sum([1 for i in range(12) if randint(1, 10) == 1])

        await ctx.send(
            f"{discord.utils.escape_mentions(ctx.message.author.display_name)} -> your seed is a {total_eyes} eye"
        )

    @findseed.error
    async def findseed_handler(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            if ctx.message.channel.id != int(
                self.bot.config[str(ctx.message.guild.id)]["bot_channel"]
            ):
                ctx.command.reset_cooldown(ctx)
                await ctx.message.delete()
                return
        else:
            await ctx.send(error)
            # await ctx.send(f"{discord.utils.escape_mentions(ctx.message.author.display_name)}, you have to wait {round(error.retry_after, 7)} seconds before using this again.")

    @commands.command()
    async def findsleep(self, ctx):
        """Test your sleep"""
        if ctx.message.channel.id != int(
            self.bot.config[str(ctx.message.guild.id)]["bot_channel"]
        ):
            await ctx.message.delete()
            return

        # DON'T ASK!
        lessSleepMsg = [
            "gn, insomniac!",
            "counting sheep didn't work? try counting chloroform vials!",
            "try a glass of water",
            "some decaf coffee might do the trick!",
        ]

        moreSleepMsg = [
            "waaakeee uuuppp!",
            "are they dead or asleep? I can't tell.",
            "wake up, muffin head",
            "psst... coffeeee \\:D",
        ]

        # Optional TODO: Create non-normal distribution
        sleepHrs = randint(0, 24)

        # Add extra comment based on number of sleepHrs
        if sleepHrs == 0:
            await ctx.send(
                f"{discord.utils.escape_mentions(ctx.message.author.display_name)} -> your sleep is 0 hours long - nice try \:D"
            )
        elif sleepHrs <= 5:
            if sleepHrs == 1:
                s = ""
            else:
                s = "s"
            await ctx.send(
                f"{discord.utils.escape_mentions(ctx.message.author.display_name)} -> your sleep is {sleepHrs} hour{s} long - {lessSleepMsg[randint(0, len(lessSleepMsg) - 1)]}"
            )
        else:
            await ctx.send(
                f"{discord.utils.escape_mentions(ctx.message.author.display_name)} -> your sleep is {sleepHrs} hours long - {moreSleepMsg[randint(0, len(moreSleepMsg) - 1)]}"
            )

    @commands.Cog.listener()
    async def on_reaction_add(self, reaction, user):
        if (
            reaction.emoji == "⭐"
            and not reaction.message.id in self.pins
            and reaction.count >= 5
        ):
            self.pins.append(reaction.message.id)

            embed = discord.Embed(
                title="**New Starred Message**",
                description=reaction.message.content,
                colour=discord.Colour(0xB92C36),
                url=reaction.message.jump_url,
                timestamp=reaction.message.created_at,
            )

            for attachement in reaction.message.attachments:
                if attachement.height:
                    embed.set_image(url=attachement.url)
            embed.set_author(
                name=str(reaction.message.author),
                icon_url=reaction.message.author.avatar_url_as(format="png"),
            )
            embed.set_footer(text=reaction.message.id)

            # embed.add_field(name="Stars", value=reaction.count)
            channel = self.bot.get_channel(
                int(self.bot.config[str(reaction.message.guild.id)]["pins_channel"])
            )
            await channel.send(embed=embed)

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
            pass

    @commands.Cog.listener()
    async def on_member_update(self, before, after):
        if after.id == 640933433215811634:
            await after.edit(nick="JoetheSheepFucker")

    @commands.Cog.listener()
    async def on_message(self, message):
        if not message.guild:
            return
        if message.author.bot:
            return
        badWords = ["fair", "ⓕⓐⓘⓡ"]
        count = 0
        year = datetime.date.today().year

        coolKids = [
            [
                "Cameron",
                self.bot.get_user(468262902969663488),
                datetime.date(year, 10, 8),
            ],
            ["Indy", self.bot.get_user(274923326890311691), datetime.date(year, 9, 10)],
            ["Kai", self.bot.get_user(199070670221475842), datetime.date(year, 11, 20)],
            ["Luca", self.bot.get_user(99457716614885376), datetime.date(year, 11, 5)],
            ["Max", self.bot.get_user(543958509243596800), datetime.date(year, 11, 10)],
            [
                "Daniel",
                self.bot.get_user(264121998173536256),
                datetime.date(year, 7, 6),
            ],
            [
                "Jake",
                self.bot.get_user(400344183333847060),
                datetime.date(year, 11, 10),
            ],
            [
                "Nevaeh",
                self.bot.get_user(738279874749530172),
                datetime.date(year, 11, 5),
            ],
            # idk if she goes by her irl name but I'm sticking with it for the sake of uniformity
            # also idk how to pronounce prakxo
            # EDIT: Seems like real names are the standard now lol
            # its just a name, aliases are stupid
            [
                "Samantha",
                self.bot.get_user(226312219787264000),
                datetime.date(year, 6, 24),
            ],
            [
                "Scott",
                self.bot.get_user(223937483774230528),
                datetime.date(year, 6, 23),
            ],
            ["Ben", self.bot.get_user(329538915805691905), datetime.date(year, 6, 24)],
            [
                "Thomas",
                self.bot.get_user(280428276810383370),
                datetime.date(year, 9, 29),
            ],
            [
                "Samantha",  # This one is Zyemlus
                self.bot.get_user(536071288859656193),
                datetime.date(year, 8, 23),
            ],
            [
                "Landen",
                self.bot.get_user(654025117025828885),
                datetime.date(year, 8, 24),
            ],
            [
                "Oceanlight",
                self.bot.get_user(615658069132836865),
                datetime.date(year, 4, 9),
            ],
            [
                "Shadowfi",
                self.bot.get_user(586664256217415681),
                datetime.date(year, 11, 14),
            ],
            ["Gold", self.bot.get_user(404873210597867541), datetime.date(year, 9, 12)],
        ]

        for coolKid in coolKids:
            if datetime.date.today() == coolKid[2]:
                try:
                    for i in range(self.tries):
                        await coolKid[1].send(
                            f"Happy Birthday {coolKid[0]}! You're a boomer now! <:mangopog:730683234039365722>"
                        )
                    self.tries = 1
                except:
                    self.tries += 1

        for word in badWords:
            if word in message.content.lower().replace(" ", ""):
                count += 1
                fair = "Fair " * count
        await message.channel.send(fair)

    @commands.cooldown(1, 60, commands.BucketType.member)
    @commands.command()
    async def report(self, ctx, *, message=None):
        """Send a message to the super mods about anything"""
        if ctx.message.guild != None:
            await ctx.message.delete()
        if message == None:
            await ctx.message.author.send(
                "Please type a report to report (hehe, sounds funny)"
            )
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
                await ctx.send(
                    "https://aninternettroll.github.io/mcbeVerifierLeaderboard/"
                )

    @leaderboard.error
    async def leaderboard_handler(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            # return
            await ctx.send(
                f"{discord.utils.escape_mentions(ctx.message.author.display_name)}, you have to wait {round(error.retry_after, 2)} seconds before using this again."
            )

    @commands.cooldown(1, 60, commands.BucketType.guild)
    @commands.command()
    async def someone(self, ctx):
        """Discord's mistake"""
        if ctx.channel.id != int(
            self.bot.config[str(ctx.message.guild.id)]["fair_channel"]
        ):
            await ctx.send(choice(ctx.guild.members).mention)

    @commands.command()
    async def roll(self, ctx, pool):
        """Roll the dice"""
        await ctx.send(f"You rolled a {randint(0, int(pool))}")

    @commands.command(aliases=["commands", "allcommands"])
    async def listcommands(self, ctx):
        """List all custom commands"""
        with open("custom_commands.json", "r") as f:
            commands = json.load(f)
            output = ", ".join([*commands])
            await ctx.send(f"```List of custom commands:\n{output}```")

    @commands.command()
    async def retime(self, ctx, start_sec, end_sec, frames=0, framerate=30):
        """Retimes a run using the start/end timestamps, leftover frames, and framerate"""
        if start_sec.count(":") == 2:
            start_sec = sum(
                x * int(t) for x, t in zip([3600, 60, 1], start_sec.split(":"))
            )
        elif start_sec.count(":") == 1:
            start_sec = sum(x * int(t) for x, t in zip([60, 1], start_sec.split(":")))
        else:
            start_sec = int(start_sec)

        if end_sec.count(":") == 2:
            end_sec = sum(x * int(t) for x, t in zip([3600, 60, 1], end_sec.split(":")))
        elif end_sec.count(":") == 1:
            end_sec = sum(x * int(t) for x, t in zip([60, 1], end_sec.split(":")))
        else:
            end_sec = int(end_sec)

        await ctx.send(
            str(
                timedelta(
                    seconds=end_sec
                    - start_sec
                    + round((int(frames) / int(framerate)), 3)
                )
            ).replace("000", "")
        )


def setup(bot):
    bot.add_cog(Utils(bot))
