import datetime
import inspect
import json
import os
import sys
from random import randint

import dateutil.parser
import discord
import requests
from discord.ext import commands

current_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)
import bot


def dump(obj):
    output = ""
    for attr in dir(obj):
        output += "\nobj.%s = %r" % (attr, getattr(obj, attr))
        print("obj.%s = %r" % (attr, getattr(obj, attr)))
    return output


class MyHelpCommand(commands.MinimalHelpCommand):
    messages = [
        "As seen on TV!",
        "Awesome!",
        "100% pure!",
        "May contain nuts!",
        "Better than Prey!",
        "More polygons!",
        "Sexy!",
        "Limited edition!",
        "Flashing letters!",
        "Made by Notch!",
        "It's here!",
        "Best in class!",
        "It's finished!",
        "Kind of dragon free!",
        "Excitement!",
        "More than 500 sold!",
        "One of a kind!",
        "Heaps of hits on YouTube!",
        "Indev!",
        "Spiders everywhere!",
        "Check it out!",
        "Holy cow",
        " man!",
        "It's a game!",
        "Made in Sweden!",
        "Uses LWJGL!",
        "Reticulating splines!",
        "Minecraft!",
        "Yaaay!",
        "Singleplayer!",
        "Keyboard compatible!",
        "Undocumented!",
        "Ingots!",
        "Exploding creepers!",
        "That's no moon!",
        "l33t!",
        "Create!",
        "Survive!",
        "Dungeon!",
        "Exclusive!",
        "The bee's knees!",
        "Down with O.P.P.!",
        "Closed source!",
        "Classy!",
        "Wow!",
        "Not on steam!",
        "Oh man!",
        "Awesome community!",
        "Pixels!",
        "Teetsuuuuoooo!",
        "Kaaneeeedaaaa!",
        "Now with difficulty!",
        "Enhanced!",
        "90% bug free!",
        "Pretty!",
        "12 herbs and spices!",
        "Fat free!",
        "Absolutely no memes!",
        "Free dental!",
        "Ask your doctor!",
        "Minors welcome!",
        "Cloud computing!",
        "Legal in Finland!",
        "Hard to label!",
        "Technically good!",
        "Bringing home the bacon!",
        "Indie!",
        "GOTY!",
        "Ceci n'est pas une title screen!",
        "Euclidian!",
        "Now in 3D!",
        "Inspirational!",
        "Herregud!",
        "Complex cellular automata!",
        "Yes",
        " sir!",
        "Played by cowboys!",
        "OpenGL 1.2!",
        "Thousands of colors!",
        "Try it!",
        "Age of Wonders is better!",
        "Try the mushroom stew!",
        "Sensational!",
        "Hot tamale",
        " hot hot tamale!",
        "Play him off",
        " keyboard cat!",
        "Guaranteed!",
        "Macroscopic!",
        "Bring it on!",
        "Random splash!",
        "Call your mother!",
        "Monster infighting!",
        "Loved by millions!",
        "Ultimate edition!",
        "Freaky!",
        "You've got a brand new key!",
        "Water proof!",
        "Uninflammable!",
        "Whoa",
        " dude!",
        "All inclusive!",
        "Tell your friends!",
        "NP is not in P!",
        "Notch <3 ez!",
        "Music by C418!",
        "Livestreamed!",
        "Haunted!",
        "Polynomial!",
        "Terrestrial!",
        "All is full of love!",
        "Full of stars!",
        "Scientific!",
        "Cooler than Spock!",
        "Collaborate and listen!",
        "Never dig down!",
        "Take frequent breaks!",
        "Not linear!",
        "Han shot first!",
        "Nice to meet you!",
        "Buckets of lava!",
        "Ride the pig!",
        "Larger than Earth!",
        "sqrt(-1) love you!",
        "Phobos anomaly!",
        "Punching wood!",
        "Falling off cliffs!",
        "0% sugar!",
        "150% hyperbole!",
        "Synecdoche!",
        "Let's danec!",
        "Seecret Friday update!",
        "Reference implementation!",
        "Lewd with two dudes with food!",
        "Kiss the sky!",
        "20 GOTO 10!",
        "Verlet intregration!",
        "Peter Griffin!",
        "Do not distribute!",
        "Cogito ergo sum!",
        "4815162342 lines of code!",
        "A skeleton popped out!",
        "The Work of Notch!",
        "The sum of its parts!",
        "BTAF used to be good!",
        "I miss ADOM!",
        "umop-apisdn!",
        "OICU812!",
        "Bring me Ray Cokes!",
        "Finger-licking!",
        "Thematic!",
        "Pneumatic!",
        "Sublime!",
        "Octagonal!",
        "Une baguette!",
        "Gargamel plays it!",
        "Rita is the new top dog!",
        "SWM forever!",
        "Representing Edsbyn!",
        "Matt Damon!",
        "Supercalifragilisticexpialidocious!",
        "Consummate V's!",
        "Cow Tools!",
        "Double buffered!",
        "Fan fiction!",
        "Flaxkikare!",
        "Jason! Jason! Jason!",
        "Hotter than the sun!",
        "Internet enabled!",
        "Autonomous!",
        "Engage!",
        "Fantasy!",
        "DRR! DRR! DRR!",
        "Kick it root down!",
        "Regional resources!",
        "Woo",
        " facepunch!",
        "Woo",
        " somethingawful!",
        "Woo",
        " /v/!",
        "Woo",
        " tigsource!",
        "Woo",
        " minecraftforum!",
        "Woo",
        " worldofminecraft!",
        "Woo",
        " reddit!",
        "Woo",
        " 2pp!",
        "Google anlyticsed!",
        "Now supports åäö!",
        "Give us Gordon!",
        "Tip your waiter!",
        "Very fun!",
        "12345 is a bad password!",
        "Vote for net neutrality!",
        "Lives in a pineapple under the sea!",
        "MAP11 has two names!",
        "Omnipotent!",
        "Gasp!",
        "...!",
        "Bees",
        " bees",
        " bees",
        " bees!",
        "Jag känner en bot!",
        "This text is hard to read if you play the game at the default resolution",
        " but at 1080p it's fine!",
        "Haha",
        " LOL!",
        "Hampsterdance!",
        "Switches and ores!",
        "Menger sponge!",
        "idspispopd!",
        "Eple (original edit)!",
        "So fresh",
        " so clean!",
        "Slow acting portals!",
        "Try the Nether!",
        "Don't look directly at the bugs!",
        "Oh",
        " ok",
        " Pigmen!",
        "Finally with ladders!",
        "Scary!",
        "Play Minecraft",
        " Watch Topgear",
        " Get Pig!",
        "Twittered about!",
        "Jump up",
        " jump up",
        " and get down!",
        "Joel is neat!",
        "A riddle",
        " wrapped in a mystery!",
        "Huge tracts of land!",
        "Welcome to your Doom!",
        "Stay a while",
        " stay forever!",
        "Stay a while and listen!",
        "Treatment for your rash!",
        '"Autological" is!',
        "Information wants to be free!",
        '"Almost never" is an interesting concept!',
        "Lots of truthiness!",
        "The creeper is a spy!",
        "Turing complete!",
        "It's groundbreaking!",
        "Let our battle's begin!",
        "The sky is the limit!",
        "Jeb has amazing hair!",
        "Ryan also has amazing hair!",
        "Casual gaming!",
        "Undefeated!",
        "Kinda like Lemmings!",
        "Follow the train",
        " CJ!",
        "Leveraging synergy!",
        "This message will never appear on the splash screen",
        " isn't that weird?",
        "DungeonQuest is unfair!",
        "110813!",
        "90210!",
        "Check out the far lands!",
        "Tyrion would love it!",
        "Also try VVVVVV!",
        "Also try Super Meat Boy!",
        "Also try Terraria!",
        "Also try Mount And Blade!",
        "Also try Project Zomboid!",
        "Also try World of Goo!",
        "Also try Limbo!",
        "Also try Pixeljunk Shooter!",
        "Also try Braid!",
        "That's super!",
        "Bread is pain!",
        "Read more books!",
        "Khaaaaaaaaan!",
        "Less addictive than TV Tropes!",
        "More addictive than lemonade!",
        "Bigger than a bread box!",
        "Millions of peaches!",
        "Fnord!",
        "This is my true form!",
        "Totally forgot about Dre!",
        "Don't bother with the clones!",
        "Pumpkinhead!",
        "Hobo humping slobo babe!",
        "Made by Jeb!",
        "Has an ending!",
        "Finally complete!",
        "Feature packed!",
        "Boots with the fur!",
        "Stop",
        " hammertime!",
        "Testificates!",
        "Conventional!",
        "Homeomorphic to a 3-sphere!",
        "Doesn't avoid double negatives!",
        "Place ALL the blocks!",
        "Does barrel rolls!",
        "Meeting expectations!",
        "PC gaming since 1873!",
        "Ghoughpteighbteau tchoghs!",
        "Déjà vu!",
        "Déjà vu!",
        "Got your nose!",
        "Haley loves Elan!",
        "Afraid of the big",
        " black bat!",
        "Doesn't use the U-word!",
        "Child's play!",
        "See you next Friday or so!",
        "From the streets of Södermalm!",
        "150 bpm for 400000 minutes!",
        "Technologic!",
        "Funk soul brother!",
        "Pumpa kungen!",
        "日本ハロー！",
        "한국 안녕하세요!",
        "Helo Cymru!",
        "Cześć Polsko!",
        "你好中国！",
        "Привет Россия!",
        "Γεια σου Ελλάδα!",
        "My life for Aiur!",
        "Lennart lennart = new Lennart();",
        "I see your vocabulary has improved!",
        "Who put it there?",
        "You can't explain that!",
        "if not ok then return end",
        "§1C§2o§3l§4o§5r§6m§7a§8t§9i§ac",
        "§kFUNKY LOL",
        "SOPA means LOSER in Swedish!",
        "Big Pointy Teeth!",
        "Bekarton guards the gate!",
        "Mmmph",
        " mmph!",
        "Don't feed avocados to parrots!",
        "Swords for everyone!",
        "Plz reply to my tweet!",
        ".party()!",
        "Take her pillow!",
        "Put that cookie down!",
        "Pretty scary!",
        "I have a suggestion.",
        "Now with extra hugs!",
        "Now java 6!",
        "Woah.",
        "HURNERJSGER?",
        "What's up",
        " Doc?",
        "Now contains 32 random daily cats!",
        "",
    ]

    def get_command_signature(self, command):
        return f"``{self.clean_prefix}{command.qualified_name} {command.signature}``"

    def get_ending_note(self) -> str:
        return self.messages[randint(0, len(self.messages) - 1)]


class General(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._original_help_command = bot.help_command
        bot.help_command = MyHelpCommand()
        bot.help_command.cog = self

    def cog_unload(self):
        self.bot.help_command = self._original_help_command

    @commands.command()
    async def prefix(self, ctx):
        """Gets the bot prefixes"""
        prefixes = bot.get_prefix(self.bot, ctx.message)
        prefixes.pop(1)
        prefixes.pop(1)
        prefixes.pop(1)
        output = ", ".join(prefixes)

        await ctx.send(f"My prefixes are {output}")

    @commands.command()
    async def userinfo(self, ctx, user: discord.Member = None):
        """Get information about a user"""
        # await ctx.send(f"```py\n{dump(user)}```")

        if not user:
            user = ctx.message.author

        output = ""
        for i in user.roles:
            output += i.mention + " "

        if user.color.value == 0:
            color = 16777210
        else:
            color = user.color

        if user.is_avatar_animated():
            profilePic = user.avatar_url_as(format="gif")
        else:
            profilePic = user.avatar_url_as(format="png")

        embed = discord.Embed(
            title=user.name,
            description=user.mention,
            color=color,
            timestamp=ctx.message.created_at,
        )
        if user.premium_since:
            embed.add_field(name="Boosting since", value=user.premium_since.date())
        # embed.set_thumbnail(url="attachment://temp.webp")
        embed.set_thumbnail(url=profilePic)
        embed.add_field(name="Nickname", value=user.display_name, inline=False)
        embed.add_field(name="Joined on", value=user.joined_at.date(), inline=True)
        embed.add_field(name="Status", value=user.status, inline=True)
        embed.add_field(
            name="Created account on", value=user.created_at.date(), inline=True
        )
        embed.add_field(name="Roles", value=output, inline=True)
        embed.set_footer(text=f"ID: {user.id}")
        await ctx.send(embed=embed)
        # os.remove("temp.webp")
        # os.remove("temp.png")

    @commands.command()
    async def coop(self, ctx, *, user: discord.Member = None):
        """Get the coop gang role"""
        if not user:
            user = ctx.message.author
        else:
            user = self.bot.get_user(int(user))

        coop_role = ctx.guild.get_role(
            int(self.bot.config[str(ctx.message.guild.id)]["coop_roleID"])
        )

        if coop_role in user.roles:
            await user.remove_roles(coop_role)
            await ctx.send("You have left coop gang")
        else:
            await user.add_roles(coop_role)
            await ctx.send("You are now in the coop gang")

    @commands.command()
    async def serverinfo(self, ctx, guild=None):
        """Get information about the server you are in"""
        if not guild:
            guild = ctx.message.guild
        else:
            print(type(guild))
            guild = self.bot.get_guild(int(guild))

        if guild.owner.color.value == 0:
            color = 16777210
        else:
            color = guild.owner.color

        emojiList = " "
        for i in guild.emojis:
            emojiList += str(i) + " "

        if guild.is_icon_animated():
            serverIcon = guild.icon_url_as(format="gif")
        else:
            serverIcon = guild.icon_url_as(format="png")

        inactiveMembers = await guild.estimate_pruned_members(days=7)

        embed = discord.Embed(
            title=guild.name,
            description=guild.description,
            color=color,
            timestamp=ctx.message.created_at,
        )
        if guild.premium_subscription_count == 0:
            pass
        else:
            if guild.premium_subscription_count == 1:
                embed.add_field(
                    name="Boosted by:",
                    value=f"{guild.premium_subscription_count} member",
                    inline=True,
                )
            else:
                embed.add_field(
                    name="Boosted by:",
                    value=f"{guild.premium_subscription_count} members",
                    inline=True,
                )
        if guild.premium_subscribers:
            boosters = ""
            for i in guild.premium_subscribers:
                boosters += i.mention + " "
            embed.add_field(name="Boosted by:", value=boosters, inline=True)
        embed.set_thumbnail(url=serverIcon)
        embed.set_image(url=guild.splash_url_as(format="png"))
        embed.add_field(name="Created on", value=guild.created_at.date(), inline=True)
        embed.add_field(name="Members", value=guild.member_count, inline=True)
        # embed.add_field(name="Emojis", value=emojiList, inline=True)
        embed.add_field(name="Owner", value=guild.owner.mention, inline=True)
        embed.add_field(
            name="Members who haven't been online in 7 days:",
            value=inactiveMembers,
            inline=True,
        )
        embed.set_footer(text=f"ID: {guild.id}")
        await ctx.send(embed=embed)

    @commands.command()
    async def xboxuser(self, ctx, *, gamertag=None):
        """Get information about an xbox live user"""
        if not gamertag:
            await ctx.send("You need to specify a gamer, gamer")
            return

        async with self.bot.session.get(
            f"https://xbl-api.prouser123.me/profile/gamertag/{gamertag}"
        ) as r:
            gamer = json.loads(await r.text())

            try:
                await ctx.send(f"{gamer['error']}: {gamer['message']}")
                return
            except KeyError:
                pass

            for i in gamer["profileUsers"][0]["settings"]:
                if i["id"] == "GameDisplayName":
                    gameName = i["value"]
                    continue
                if i["id"] == "AppDisplayPicRaw":
                    picUrl = i["value"]
                    continue
                if i["id"] == "Gamerscore":
                    Gamerscore = i["value"] + "<:gamerscore:727131234534424586>"
                    continue
                if i["id"] == "AccountTier":
                    accountTier = i["value"]
                    continue
                if i["id"] == "XboxOneRep":
                    reputation = i["value"]
                    continue
                if i["id"] == "PreferredColor":
                    color = int(
                        json.loads(requests.get(i["value"]).text)["primaryColor"], 16
                    )
                    continue
                if i["id"] == "Location":
                    location = i["value"]
                    continue
                if i["id"] == "Bio":
                    # if len(i["value"]) == 0:
                    # 	Bio = "Unknown"
                    # else:
                    Bio = i["value"]
                    continue
                if i["id"] == "Watermarks":
                    Watermarks = i["value"]
                    continue
                if i["id"] == "RealName":
                    RealName = i["value"]
                    continue

            embed = discord.Embed(
                title=gameName,
                description=Bio,
                color=color,
                timestamp=ctx.message.created_at,
            )
            embed.set_thumbnail(url=picUrl)
            embed.add_field(name="Gamerscore", value=Gamerscore, inline=True)
            if len(location) != 0:
                embed.add_field(name="Location", value=location, inline=True)
            if len(Watermarks) != 0:
                embed.add_field(name="Watermarks", value=Watermarks, inline=True)
            embed.add_field(name="Account Tier", value=accountTier, inline=True)
            embed.add_field(name="Reputation", value=reputation, inline=True)
            await ctx.send(embed=embed)

    @commands.command(hidden=True)
    async def xboxpresence(self, ctx, *, gamertag=None):
        if not gamertag:
            await ctx.send("You need to specify a gamer, gamer")
            return

        async with self.bot.session.get(
            f"https://xbl-api.prouser123.me/presence/gamertag/{gamertag}"
        ) as r:
            gamer = json.loads(await r.text())

            try:
                await ctx.send(f"{gamer['error']}: {gamer['message']}")
                return
            except KeyError:
                pass

            state = gamer["state"]

            try:
                game = json.loads(
                    requests.get(
                        f"https://xbl-api.prouser123.me/titleinfo/{gamer['lastSeen']['titleId']}"
                    ).text
                )
                gameName = game["titles"][0]["name"]
                gamePic = game["titles"][0]["images"][4]["url"]
                timestamp = dateutil.parser.isoparse(gamer["lastSeen"]["timestamp"])
                lastSeen = True
            except Exception as e:
                print(e)
                lastSeen = False

            if lastSeen:
                embed = discord.Embed(
                    title=gamer["gamertag"], description=state, timestamp=timestamp
                )
                embed.set_thumbnail(url=gamePic)
                embed.add_field(name="Game", value=gameName, inline=True)
                await ctx.send(embed=embed)
            else:
                embed = discord.Embed(
                    title=gamer["gamertag"],
                    description=state,
                    timestamp=ctx.message.created_at,
                )
                await ctx.send(embed=embed)

    @commands.command()
    async def compile(self, ctx, language=None, *, code=None):
        """Compile code from a variety of programming languages, powered by <https://wandbox.org/>"""
        """
		listRequest = requests.get("https://wandbox.org/api/list.json")
		compilerList = json.loads(listRequest.text)

		for i in compilerList:
			if i["language"] == language:
				compiler = i["name"]
				print(compiler)
		"""
        compilers = {
            "bash": "bash",
            "c": "gcc-head-c",
            "c#": "dotnetcore-head",
            "coffeescript": "coffeescript-head",
            "cpp": "gcc-head",
            "elixir": "elixir-head",
            "go": "go-head",
            "java": "openjdk-head",
            "javascript": "nodejs-head",
            "lua": "lua-5.3.4",
            "perl": "perl-head",
            "php": "php-head",
            "python": "cpython-3.8.0",
            "ruby": "ruby-head",
            "rust": "rust-head",
            "sql": "sqlite-head",
            "swift": "swift-5.0.1",
            "typescript": "typescript-3.5.1",
            "vim-script": "vim-head",
        }
        if not language:
            await ctx.send(f"```json\n{json.dumps(compilers, indent=4)}```")
        if not code:
            await ctx.send("No code found")
            return
        try:
            compiler = compilers[language.lower()]
        except KeyError:
            await ctx.send("Language not found")
            return
        body = {"compiler": compiler, "code": code, "save": True}
        head = {"Content-Type": "application/json"}
        async with ctx.typing():
            async with self.bot.session.post(
                "https://wandbox.org/api/compile.json",
                headers=head,
                data=json.dumps(body),
            ) as r:
                # r = requests.post("https://wandbox.org/api/compile.json", headers=head, data=json.dumps(body))
                try:
                    response = json.loads(await r.text())
                    # await ctx.send(f"```json\n{json.dumps(response, indent=4)}```")
                    print(f"```json\n{json.dumps(response, indent=4)}```")
                except json.decoder.JSONDecodeError:
                    await ctx.send(f"```json\n{r.text}```")

                try:
                    embed = discord.Embed(title="Compiled code")
                    embed.add_field(
                        name="Output",
                        value=f'```{response["program_message"]}```',
                        inline=False,
                    )
                    embed.add_field(
                        name="Exit code", value=response["status"], inline=True
                    )
                    embed.add_field(
                        name="Link",
                        value=f"[Permalink]({response['url']})",
                        inline=True,
                    )
                    await ctx.send(embed=embed)
                except KeyError:
                    await ctx.send(f"```json\n{json.dumps(response, indent=4)}```")


def setup(bot):
    bot.add_cog(General(bot))
