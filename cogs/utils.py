import asyncio
import datetime
import json
import os
import subprocess
import unicodedata
from collections import namedtuple
from datetime import timedelta
from math import floor
from random import choice, randint

import discord
from discord.ext import commands
from pytz import exceptions, timezone

# forgot to import this (randint) and ended up looking mentally unstable
# troll literally pointed out atleast 4 things I did wrong in 3 lines of code


# from PIL.Image import core as Image
# import image as Image
# from PIL import Image, ImageFilter
# from selenium import webdriver
# from selenium.webdriver.chrome.options import Options

# def set_viewport_size(driver, width, height):
#     window_size = driver.execute_script(
#         """
# 		return [window.outerWidth - window.innerWidth + arguments[0],
# 		  window.outerHeight - window.innerHeight + arguments[1]];
# 		""",
#         width,
#         height,
#     )
#     driver.set_window_size(*window_size)


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


# def save_leaderboard():
#     DRIVER = "/usr/lib/chromium-browser/chromedriver"
#     chrome_options = Options()
#     chrome_options.add_argument("--disable-dev-shm-usage")
#     chrome_options.add_argument("--headless")
#     chrome_options.add_argument("--no-sandbox")
#     chrome_options.add_argument("--disable-gpu")
#     # chrome_options.binary_location = ""
#     driver = webdriver.Chrome(DRIVER, chrome_options=chrome_options)
#     set_viewport_size(driver, 1000, 1100)
#     driver.get("https://aninternettroll.github.io/mcbeVerifierLeaderboard/")
#     screenshot = driver.find_element_by_id("table").screenshot("leaderboard.png")
#     driver.quit()
#     # transparency time
#     img = Image.open("leaderboard.png")
#     img = img.convert("RGB")
#     pallette = Image.open("palette.png")
#     pallette = pallette.convert("P")
#     img = img.quantize(colors=256, method=3, kmeans=0, palette=pallette)
#     img = img.convert("RGBA")
#     datas = img.getdata()
#
#     newData = []
#     for item in datas:
#         if item[0] == 255 and item[1] == 255 and item[2] == 255:
#             newData.append((255, 255, 255, 0))
#         else:
#             newData.append(item)
#
#     img.putdata(newData)
#     """
# 	img = img.filter(ImageFilter.SHARPEN)
# 	img = img.filter(ImageFilter.SHARPEN)
# 	img = img.filter(ImageFilter.SHARPEN)
# 	"""
#     # height, width = img.size
#     # img = img.resize((height*10,width*10), resample=Image.BOX)
#     img.save("leaderboard.png", "PNG")


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
            # What a fraud! They didn't use their real name.
            615658069132836865: -12,
        }

        if ctx.author.id in rigged_findseed:
            total_eyes = rigged_findseed[ctx.author.id]
        else:
            total_eyes = sum(1 for i in range(12) if randint(1, 10) == 1)

        await ctx.send(
            f"{discord.utils.escape_mentions(ctx.message.author.display_name)} -> your seed is a {total_eyes} eye"
        )

    @commands.command()
    async def findsleep(self, ctx):
        """Test your sleep"""
        if ctx.message.channel.id != int(
            self.bot.config[str(ctx.message.guild.id)]["bot_channel"]
        ):
            await ctx.message.delete()
            return

        # DON'T ASK!
        lessSleepMsg = (
            "gn, insomniac!",
            "counting sheep didn't work? try counting chloroform vials!",
            "try a glass of water",
            "some decaf coffee might do the trick!",
        )

        moreSleepMsg = (
            "waaakeee uuuppp!",
            "are they dead or asleep? I can't tell.",
            "wake up, muffin head",
            "psst... coffeeee \\:D",
        )

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
            await msg.channel.send(
                f"{member.mention}\n"
                + "controller is allowed on mobile\n"
                + "keyboard and mouse is allowed on console\n"
                + "submit the run as the physical device you played on"
            )
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
        if (
            "<@!280428276810383370>" in message.content
            or "<@280428276810383370>" in message.content
        ):
            await message.channel.send("<:MangoPing:760286455238361129>")
        badWords = ("fair", "ⓕⓐⓘⓡ")
        count = 0
        year = datetime.date.today().year
        CoolKids = namedtuple(
            "CoolKid",
            [
                "name",
                "user",
                "bday",
            ],
        )

        coolKids = (
            CoolKids(
                name="Cameron",
                user=self.bot.get_user(468262902969663488),
                bday=datetime.date(year, 10, 8),
            ),
            CoolKids(
                name="Indy",
                user=self.bot.get_user(274923326890311691),
                bday=datetime.date(year, 9, 10),
            ),
            CoolKids(
                name="Kai",
                user=self.bot.get_user(199070670221475842),
                bday=datetime.date(year, 11, 26),
            ),
            CoolKids(
                name="Luca",
                user=self.bot.get_user(99457716614885376),
                bday=datetime.date(year, 11, 5),
            ),
            CoolKids(
                name="Max",
                user=self.bot.get_user(543958509243596800),
                bday=datetime.date(year, 11, 10),
            ),
            CoolKids(
                name="Daniel",
                user=self.bot.get_user(264121998173536256),
                bday=datetime.date(year, 7, 6),
            ),  # Mistaken
            CoolKids(
                name="Jake",
                user=self.bot.get_user(400344183333847060),
                bday=datetime.date(year, 11, 10),
            ),
            CoolKids(
                name="Faith",
                user=self.bot.get_user(744383381843738633),
                bday=datetime.date(year, 11, 5),
            ),
            # Prakxo
            CoolKids(
                name="Samanta",
                user=self.bot.get_user(226312219787264000),
                bday=datetime.date(year, 6, 24),
            ),
            CoolKids(
                name="Scott",
                user=self.bot.get_user(223937483774230528),
                bday=datetime.date(year, 6, 23),
            ),
            CoolKids(
                name="Kyra",
                user=self.bot.get_user(329538915805691905),
                bday=datetime.date(year, 6, 24),
            ),
            CoolKids(
                name="Thomas",
                user=self.bot.get_user(280428276810383370),
                bday=datetime.date(year, 9, 29),
            ),
            # Zyemlus
            CoolKids(
                name="Samantha",
                user=self.bot.get_user(536071288859656193),
                bday=datetime.date(year, 8, 23),
            ),
            CoolKids(
                name="Landen",
                user=self.bot.get_user(654025117025828885),
                bday=datetime.date(year, 8, 24),
            ),
            CoolKids(
                name="Oceanlight",
                user=self.bot.get_user(615658069132836865),
                bday=datetime.date(year, 4, 9),
            ),
            # Shadowfi
            CoolKids(
                name="Daniel",
                user=self.bot.get_user(586664256217415681),
                bday=datetime.date(year, 11, 14),
            ),
            CoolKids(
                name="Sawyer",
                user=self.bot.get_user(404873210597867541),
                bday=datetime.date(year, 9, 12),
            ),
            CoolKids(
                name="Marco",
                user=self.bot.get_user(299668599650648065),
                bday=datetime.date(year, 11, 12),
            ),
            CoolKids(
                name="Tyler",
                user=self.bot.get_user(619322461749641246),
                bday=datetime.date(year, 3, 4),
            ),
            CoolKids(
                name="Avery",
                user=self.bot.get_user(538824552906489874),
                bday=datetime.date(year, 10, 16),
            ),
            CoolKids(
                name="Matthew",
                user=self.bot.get_user(525365553842356225),
                bday=datetime.date(year, 1, 2),
            ),
            CoolKids(
                name="Samuel",
                user=self.bot.get_user(615235547920597150),
                bday=datetime.date(year, 12, 13),
            ),
        )

        for kid in coolKids:
            if datetime.date.today() == kid.bday:
                try:
                    for i in range(self.tries):
                        await kid.user.send(
                            f"Happy Birthday {kid.name}! You're a boomer now! <:mangopog:730683234039365722>"
                        )
                    self.tries = 1
                except:
                    self.tries += 1

        # *Don't* ask
        if message.author.id == 289721817516605440:  # An ultra special dude
            text = (
                unicodedata.normalize("NFD", message.content)
                .encode("ascii", "ignore")
                .decode("utf-8")
            )
            if "women" in text.lower() or "woman" in text.lower():
                await message.channel.send("<:shut:808843657167765546>")
        if message.reference is not None and len(message.content) == 0:
            reply = await message.channel.fetch_message(message.reference.message_id)
            if reply.is_system():

                def check(m):
                    return (
                        m.author == message.author
                        and message.reference is not None
                        and len(message.content) == 0
                    )

                try:
                    msg2 = await self.bot.wait_for("message", check=check)
                except asyncio.TimeoutError:
                    return
                reply2 = await msg2.channel.fetch_message(msg2.reference.message_id)
                if not reply2.is_system():
                    return
                muted_role = message.guild.get_role(
                    int(self.bot.config[str(message.guild.id)]["mute_role"])
                )
                await message.author.add_roles(muted_role, reason="spam")
                await message.channel.send(
                    "{0.mention} has been muted for *spam*".format(message.author)
                )
                await asyncio.sleep(300)
                await message.author.remove_roles(muted_role, reason="time's up ")

        for word in badWords:
            if word in message.content.lower().replace(" ", ""):
                # get fair object
                with open("fair.json", "r") as f:
                    fair = json.load(f)

                # if fairer's ID in fair.json
                userId = str(message.author.id)
                if userId in fair:
                    # TODO: use timezones (get this time based on timezones to fair.json - default to GMT)
                    tz = fair[userId]["timezone"]
                    today = str(datetime.datetime.now(timezone(tz)).date())
                    yesterday = str(
                        datetime.datetime.now(timezone(tz)).date() - timedelta(1)
                    )

                    # if date in json != current date
                    date = fair[userId]["date"]
                    if date != today:
                        # increment fair day
                        fairDay = fair[userId]["day"] + 1

                        fairStreak = fair[userId]["streak"]
                        # if the user faired yesterday
                        if yesterday == date:
                            fairStreak = fair[userId]["streak"] + 1
                        else:
                            fairStreak = 1
                            await message.channel.send(
                                "streak lost. <:sad:716629485449117708>"
                            )

                        # only send && update if user is fairing for the first time today
                        fair[userId] = {
                            "day": fairDay,
                            "streak": fairStreak,
                            "date": today,
                            "timezone": tz,
                        }

                        fairInfo = f"day {fair[userId]['day']}, streak {fair[userId]['streak']}"
                        await message.channel.send(fairInfo)

                # new user - not in fair.json
                else:
                    # default to GMT
                    tz = "Europe/London"
                    today = str(datetime.datetime.now(timezone(tz)).date())
                    fair[userId] = {
                        "day": 1,
                        "streak": 1,
                        "date": today,
                        "timezone": tz,
                    }

                    fairInfo = (
                        f"day {fair[userId]['day']}, streak {fair[userId]['streak']}"
                    )
                    await message.channel.send(fairInfo)

                # overwrite with new fair object
                with open("fair.json", "w") as f:
                    json.dump(fair, f, indent=4)

                count += 1
                fairMsg = "Fair " * count
        try:
            await message.channel.send(fairMsg)
        except UnboundLocalError:
            pass

    # 24 hour cooldown
    # should probably be longer - we can't have these kids cheating!
    @commands.cooldown(1, 86400, commands.BucketType.user)
    @commands.command()
    async def timezone(self, ctx, timeZone):
        """set timezone for fair days/streaks"""

        # get fair object
        with open("fair.json", "r") as f:
            fair = json.load(f)

        # if this user has faired before
        userId = str(ctx.author.id)
        if userId not in fair:
            # new user
            await ctx.send("try saying 'fair' first")
            return

        try:
            # let users timezone = input timezone (string version so as to please json)
            # use timezone() simply to see if it's valid
            tz = str(timezone(timeZone))

        except exceptions.UnknownTimeZoneError:
            await ctx.send(
                "That's not a valid timezone. You can look them up at https://kevinnovak.github.io/Time-Zone-Picker/"
            )
            return

        # set user's timezone to (verified) input zone
        fair[userId]["timezone"] = tz

        # overwrite with new fair object
        with open("fair.json", "w") as f:
            json.dump(fair, f, indent=4)

        await ctx.send(
            f"{discord.utils.escape_mentions(ctx.message.author.display_name)} your timezone has been set to {timeZone}"
        )

    @commands.cooldown(2, 60, commands.BucketType.user)
    @commands.command()
    async def fboard(self, ctx, requested: str = "streak"):
        """Show fair leaderboard (day or streak)."""
        # Get fair object.
        with open("fair.json", "r") as f:
            fair = json.load(f)

        # Detect people who didn't maintain their streak.
        for user in fair:
            tz = fair[user]["timezone"]
            try:
                currentdate = datetime.datetime.now(timezone(tz)).date()
            except:
                # Ocean put in a test timezone and it messes with stuff
                continue
            if fair[user]["date"] != str(currentdate) and fair[user]["date"] != str(
                currentdate - timedelta(1)
            ):
                fair[user]["streak"] = 1
                fair[user]["date"] = str(currentdate)
                try:
                    # It seems like people don't like spam pings

                    # await ctx.send(
                    #    self.bot.get_user(int(user)).mention
                    #    + ": You lost your streak! <:sad:716629485449117708>"
                    # )

                    pass
                except:
                    # User left the server so the bot can't find them
                    continue

        with open("fair.json", "w") as f:
            json.dump(fair, f, indent=4)

        leaderboard = []

        # String the requested info with its respective user and store it in our list
        if requested.lower() == "day":
            for user in fair:
                leaderboard.append(str(fair[user]["day"]) + " " + user)
            flag = "Day"

        elif requested.lower() == "streak":
            for user in fair:
                leaderboard.append(str(fair[user]["streak"]) + " " + user)
            flag = "Streak"

        else:
            await ctx.send('Request the leaderboard by "day" or "streak".')
            return

        # Sort the "info + user" strings as ints.
        leaderboard.sort(reverse=True, key=lambda pair: int(pair.split(" ")[0]))

        text = ""
        embed = discord.Embed(
            title="Fair Leaderboard", color=7853978, timestamp=ctx.message.created_at
        )

        addNewField = True
        callerid = ctx.message.author.id

        # Get the top 10 entries and extract the info and user from each string
        for i in range(10):
            entry = leaderboard[i].split(" ")[0]
            userstr = leaderboard[i].split(" ")[1]
            # If caller is in top 10, then we highlight their entry
            if str(callerid) == userstr:
                text += f"**{i+1}. {self.bot.get_user(int(userstr))}: {entry}** \n"
                addNewField = False
            else:
                text += f"{i+1}. {self.bot.get_user(int(userstr))}: {entry} \n"

        if not str(callerid) in fair:
            addNewField = False

        # If caller is not in top 10, we add a new field with their place on the leaderboard and another one with number of people that have the same value (tied)
        if addNewField:
            if flag == "Day":
                value = fair[str(callerid)]["day"]
            elif flag == "Streak":
                value = fair[str(callerid)]["streak"]

            # Binary searches for caller in leaderboard. First we find leftmost element that has [value] in it.
            left = 0
            right = len(leaderboard)
            while left < right:
                middle = floor((left + right) / 2)
                if int(leaderboard[middle].split(" ")[0]) > value:
                    left = middle + 1
                else:
                    right = middle

            leftIndex = left

            # Now we find the rightmost one.
            left = 0
            right = len(leaderboard)
            while left < right:
                middle = floor((left + right) / 2)
                if int(leaderboard[middle].split(" ")[0]) < value:
                    right = middle
                else:
                    left = middle + 1

            rightIndex = right

            cutlist = leaderboard[leftIndex:right]
            cutlist.sort(key=lambda pair: int(pair.split(" ")[1]))

            # Finally, we find the caller id index
            left = 0
            right = len(cutlist) - 1
            while left <= right:
                middle = floor((left + right) / 2)
                if int(cutlist[middle].split(" ")[1]) < callerid:
                    left = middle + 1
                elif int(cutlist[middle].split(" ")[1]) > callerid:
                    right = middle - 1
                else:
                    callerIndex = middle
                    break

            entry = cutlist[callerIndex].split(" ")[0]
            userstr = cutlist[callerIndex].split(" ")[1]

            # If caller is the 11th place on the leaderboard, highlight their entry.
            if callerIndex + leftIndex == 10:
                text += f"**11. {self.bot.get_user(int(userstr))}: {entry}** \n"
            else:
                text += f"\n{callerIndex + leftIndex + 1}. {self.bot.get_user(int(userstr))}: {entry} \nRange of positions with value {entry}: {leftIndex+1} - {rightIndex}\n"

        embed.add_field(name=flag, value=text, inline=False)

        await ctx.send(embed=embed)

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
            #            try:
            #                lbFunc = functools.partial(save_leaderboard)
            #                await self.bot.loop.run_in_executor(None, lbFunc)
            #                await ctx.send(file=discord.File("leaderboard.png"))
            #            except:
            await ctx.send("https://aninternettroll.github.io/mcbeVerifierLeaderboard/")

    @commands.cooldown(1, 60, commands.BucketType.guild)
    @commands.command()
    async def someone(self, ctx):
        """Discord's mistake"""

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

    @commands.command(aliases=["calc"])
    async def math(self, ctx, *, eqn: str):
        if '"' in eqn or "print" in eqn:
            return
        try:
            # Allow for proper absolute value notation
            pipes = eqn.count("|")
            eqn = eqn.replace("|", "abs(", pipes // 2).replace("|", ")", pipes // 2)

            with open("bc_input.bc", "w") as f:
                f.write(eqn)
            result = subprocess.check_output("utils/math", shell=True)
            os.remove("bc_input.bc")

            await ctx.send(result.decode("utf-8").replace("\\\n", "").strip())
        except subprocess.CalledProcessError as err:
            print(err)
            await ctx.send("Something went wrong")

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


async def setup(bot):
    await bot.add_cog(Utils(bot))
