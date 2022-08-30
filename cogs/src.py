import json
from datetime import timedelta
from pathlib import Path

import discord
import requests
from discord.ext import commands, tasks


class SubmittedRun:
    def __init__(
        self, game, _id, category, video, players, duration, _type, link, values
    ):
        self.game = game
        self._id = _id
        self.category = category
        self.video = video
        self.players = players
        self.duration = duration
        self._type = _type
        self.link = link
        self.values = values


async def rejectRun(self, apiKey, ctx, run, reason):
    await ctx.message.delete()
    run = run.split("/")[-1]
    reject = {"status": {"status": "rejected", "reason": reason}}
    r = requests.put(
        f"https://www.speedrun.com/api/v1/runs/{run}/status",
        headers={
            "X-API-Key": apiKey,
            "Accept": "application/json",
            "User-Agent": "mcbeDiscordBot/1.0",
        },
        data=json.dumps(reject),
    )
    if r.status_code == 200 or r.status_code == 204:
        await ctx.send(f"Run rejected succesfully for `{reason}`")
    else:
        await ctx.send("Something went wrong")
        await ctx.message.author.send(
            f"```json\n{json.dumps(json.loads(r.text),indent=4)}```"
        )


async def approveRun(self, apiKey, ctx, run, reason=None):
    await ctx.message.delete()
    run = run.split("/")[-1]
    if reason == None:
        approve = {"status": {"status": "verified"}}
    else:
        approve = {"status": {"status": "verified", "reason": reason}}
    r = requests.put(
        f"https://www.speedrun.com/api/v1/runs/{run}/status",
        headers={
            "X-API-Key": apiKey,
            "Accept": "application/json",
            "User-Agent": "mcbeDiscordBot/1.0",
        },
        data=json.dumps(approve),
    )
    if r.status_code == 200 or r.status_code == 204:
        await ctx.send("Run approved succesfully")
    else:
        await ctx.send("Something went wrong")
        await ctx.message.author.send(
            f"```json\n{json.dumps(json.loads(r.text),indent=4)}```"
        )


async def deleteRun(self, apiKey, ctx, run):
    await ctx.message.delete()
    run = run.split("/")[-1]
    r = requests.delete(
        f"https://www.speedrun.com/api/v1/runs/{run}",
        headers={
            "X-API-Key": apiKey,
            "Accept": "application/json",
            "User-Agent": "mcbeDiscordBot/1.0",
        },
    )
    if r.status_code == 200 or r.status_code == 204:
        await ctx.send("Run deleted succesfully")
    else:
        await ctx.send("Something went wrong")
        await ctx.message.author.send(
            f"```json\n{json.dumps(json.loads(r.text),indent=4)}```"
        )


async def pendingRuns(self, ctx):
    def banned_player_coop(run) -> bool:
        for player in run.players:
            if player in self.bot.runs_blacklist["players"]:
                return True
        return False

    def duplicate_run(run) -> bool:
        for pending_run in pending_runs:
            if (
                run._id != pending_run._id
                and run.category == pending_run.category
                and run.video == pending_run.video
                and run.duration == pending_run.duration
                and run.values == pending_run.values
            ):
                return True
        return False

    def get_player_name(player) -> str:
        if player["rel"] == "user":
            return player["names"]["international"]
        else:
            return player["name"]

    mcbe_runs = 0
    mcbeil_runs = 0
    mcbece_runs = 0
    pending_runs = []
    runs_to_reject = []
    game_ids = ("yd4ovvg1", "v1po7r76")  # [mcbe, mcbece]
    head = {"Accept": "application/json", "User-Agent": "mcbeDiscordBot/1.0"}

    for game in game_ids:
        runs = []
        async with self.bot.session.get(
            f"https://www.speedrun.com/api/v1/runs?game={game}&status=new&max=200&embed=category,players,level&orderby=submitted",
            headers=head,
        ) as temp:
            while True:
                temp_json = await temp.json()
                runs.extend(temp_json["data"])
                if (
                    "pagination" not in temp_json
                    or temp_json["pagination"]["size"] < 200
                ):
                    break
                temp = await self.bot.session.get(
                    {
                        item["rel"]: item["uri"]
                        for item in temp_json["pagination"]["links"]
                    }["next"],
                    headers=head,
                )

        for run in runs:
            _id = run["id"]
            duration = timedelta(seconds=run["times"]["realtime_t"])

            if run["videos"]:
                try:
                    video = run["videos"]["links"][0]["uri"]
                except KeyError:
                    video = run["videos"]["text"]
            else:
                video = None

            # Get the category name for each run, while specifiying if its a full game, il, or cat ext run
            if run["level"]["data"] != []:
                category = run["level"]["data"]["name"]
                if game == "yd4ovvg1":
                    _type = "Individual Level"
            else:
                category = run["category"]["data"]["name"]
                if game == "yd4ovvg1":
                    _type = "Full Game Run"

            if game == "v1po7r76":
                _type = "Category Extension"

            # Set players to a string if solo, or a list if coop
            if len(run["players"]["data"]) == 1:
                players = get_player_name(run["players"]["data"][0])
            else:
                players = tuple(
                    map(lambda player: get_player_name(player), run["players"]["data"])
                )

            # Get the values of the run for the duplicate remover
            values = run["values"]

            link = run["weblink"]

            pending_run = SubmittedRun(
                game, _id, category, video, players, duration, _type, link, values
            )
            pending_runs.append(pending_run)

    for run in pending_runs:
        # Reject run if video is blacklisted
        if run.video.split("/")[-1].split("=")[-1] in self.bot.runs_blacklist["videos"]:
            runs_to_reject.append((run, "Detected as spam by our automatic filter."))

        # Reject run if player is banned (solo runs)
        elif (
            type(run.players) == str
            and run.players in self.bot.runs_blacklist["players"]
        ):
            runs_to_reject.append(
                (
                    run,
                    f"Detected as a banned player ({run.players}) run by our automatic filter.",
                )
            )

        # Reject run if player is banned (coop runs)
        elif banned_player_coop(run) == True:
            runs_to_reject.append(
                (
                    run,
                    f"Detected a banned player in the list of runners ({run.players}) by our automatic filter.",
                )
            )

        # Reject run if duplicate submission
        elif duplicate_run(run) == True:
            runs_to_reject.append(
                (run, "Detected as a duplicate submission by our automatic filter.")
            )
            pending_runs.remove(run)

        # Reject run if it's a clear fake (less than 30 second full game run, but not Kill Elder Guardian)
        elif (
            run._type == "Full Game Run"
            and "Kill Bosses Glitchless" not in run.category
            and run.duration.seconds <= 60
        ):
            runs_to_reject.append(
                (run, "Detected as a fake run by our automatic filter.")
            )

        else:
            if run._type == "Full Game Run":
                mcbe_runs += 1
            elif run._type == "Individual Level":
                mcbeil_runs += 1
            else:
                mcbece_runs += 1

            # In the case of coop, change the player names from a list to a string for prettier output
            if type(run.players) == tuple:
                run.players = ", ".join(map(str, run.players))

            embed = discord.Embed(
                title=run._type,
                url=run.link,
                description=f"{run.category} in `{str(run.duration).replace('000','')}` by **{run.players}**",
                color=0x9400D3,
            )
            await self.bot.get_channel(
                int(self.bot.config[str(ctx.message.guild.id)]["pending_channel"])
            ).send(embed=embed)

    embed_stats = discord.Embed(
        title="Pending Run Stats",
        description=f"Full Game Runs: {mcbe_runs}\nIndividual Level Runs: {mcbeil_runs}\nCategory Extension Runs: {mcbece_runs}\nTotal Runs: {mcbe_runs+mcbeil_runs+mcbece_runs}",
        color=0x000000,
    )
    await self.bot.get_channel(
        int(self.bot.config[str(ctx.message.guild.id)]["pending_channel"])
    ).send(embed=embed_stats)

    for run in runs_to_reject:
        try:
            reject = {"status": {"status": "rejected", "reason": run[1]}}
            r = requests.put(
                f"https://www.speedrun.com/api/v1/runs/{run[0]._id}/status",
                headers={
                    "X-API-Key": self.bot.config["api_key"],
                    "Accept": "application/json",
                    "User-Agent": "MCBE_Moderation_Bot/1.0",
                },
                data=json.dumps(reject),
            )
            if r.status_code in [200, 204]:
                await ctx.send(
                    f"Run rejected succesfully for `{run[1]}`\nLink: <{run[0].link}>"
                )
            else:
                await ctx.send("Something went wrong")
                await ctx.message.author.send(
                    f"```json\n{json.dumps(json.loads(r.text),indent=4)}```"
                )
        except:
            continue


async def verifyNew(self, apiKey=None, userID=None):
    if apiKey == None:
        head = {"Accept": "application/json", "User-Agent": "mcbeDiscordBot/1.0"}
    else:
        head = {
            "X-API-Key": apiKey,
            "Accept": "application/json",
            "User-Agent": "mcbeDiscordBot/1.0",
        }
    server = self.bot.get_guild(574267523869179904)
    # Troll is mentally challenged I guess ¯\_(ツ)_/¯
    RunneRole = server.get_role(574268937454223361)
    WrRole = server.get_role(583622436378116107)
    # if userID == None:
    # 	return
    # else:
    user = await self.bot.fetch_user(int(userID))
    data = json.loads(Path("./api_keys.json").read_text())

    if str(user.id) in data:
        pbs = requests.get(
            f"https://www.speedrun.com/api/v1/users/{data[str(user.id)]}/personal-bests",
            headers=head,
        )
        pbs = json.loads(pbs.text)
    else:
        r = requests.get("https://www.speedrun.com/api/v1/profile", headers=head)
        # print(r.text)
        if r.status_code >= 400:
            await user.send(f"```json\n{r.text}```")
            return
        try:
            profile = json.loads(r.text)
        except json.decoder.JSONDecodeError:
            return
        srcUserID = profile["data"]["id"]
        with open("api_keys.json", "w") as file:
            data[user.id] = srcUserID
            json.dump(data, file, indent=4)
        pbs = requests.get(profile["data"]["links"][3]["uri"], headers=head)
        pbs = json.loads(pbs.text)

    wrCounter = False
    runnerCounter = False

    for i in pbs["data"]:
        if i["place"] == 1:
            if i["run"]["game"] == "yd4ovvg1" or i["run"]["game"] == "v1po7r76":
                if not i["run"]["level"]:
                    wrCounter = True
        if i["run"]["game"] == "yd4ovvg1" or i["run"]["game"] == "v1po7r76":
            # I have no shame
            runnerCounter = True

    member = await server.fetch_member(user.id)
    if wrCounter:
        await member.add_roles(WrRole)
    else:
        await member.remove_roles(WrRole)
    if runnerCounter:
        await member.add_roles(RunneRole)
    else:
        await member.remove_roles(RunneRole)


async def verifiedCount(self, ctx, modName):
    head = {"Accept": "application/json", "User-Agent": "mcbeDiscordBot/1.0"}
    async with self.bot.session.get(
        f"https://www.speedrun.com/api/v1/users/{modName}", headers=head
    ) as r:
        if r.status != 200:
            await ctx.send(f"Could not find user {modName}")
            return
        try:
            modID = await r.json()
            modID = modID["data"]["id"]
        except:
            await ctx.send("Something went wrong")
            return

    hold = []
    async with self.bot.session.get(
        f"https://www.speedrun.com/api/v1/runs?examiner={modID}&max=200", headers=head
    ) as temp:
        while True:
            if temp.status != 200:
                await ctx.send("Something went wrong")
                return
            temp_json = await temp.json()
            hold.extend(temp_json["data"])
            if "pagination" not in temp_json or temp_json["pagination"]["size"] < 200:
                break
            temp = await self.bot.session.get(
                {item["rel"]: item["uri"] for item in temp_json["pagination"]["links"]}[
                    "next"
                ],
                headers=head,
            )

    await ctx.send(f"{modName} has verified {len(hold)} runs")


class Src(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.checker.start()

    async def is_mod(ctx):
        return ctx.author.guild_permissions.manage_channels

    @commands.cooldown(1, 600, commands.BucketType.guild)
    @commands.command(description="Posts all pending runs to #pending-runs")
    @commands.guild_only()
    async def pending(self, ctx):
        async with ctx.typing():
            await self.bot.get_channel(
                int(self.bot.config[str(ctx.message.guild.id)]["pending_channel"])
            ).purge(limit=500)
            await pendingRuns(self, ctx)

    @commands.command(description="Reject runs quickly")
    @commands.check(is_mod)
    @commands.guild_only()
    async def reject(
        self,
        ctx,
        apiKey,
        run,
        *,
        reason="Rejected using Steve. No additional reason provided",
    ):
        if apiKey == None:
            apiKey = self.bot.config["api_key"]
        await rejectRun(self, apiKey, ctx, run, reason)

    @commands.command(description="Approve runs quickly")
    @commands.check(is_mod)
    @commands.guild_only()
    async def approve(
        self,
        ctx,
        apiKey,
        run,
        *,
        reason="Approved using Steve. No additional reason provided",
    ):
        if apiKey == None:
            apiKey = self.bot.config["api_key"]
        await approveRun(self, apiKey, ctx, run, reason)

    @commands.command(description="Delete runs quickly")
    async def delete(self, ctx, apiKey, run):
        await deleteRun(self, apiKey, ctx, run)

    @commands.command()
    async def verify(self, ctx, apiKey=None, userID=None):
        self.bot.messageBlacklist.append(ctx.message.id)
        if apiKey == None:
            data = json.loads(Path("./api_keys.json").read_text())
            if not str(ctx.author.id) in data:
                await ctx.send(
                    f"Please try this command again by getting an api key from https://www.speedrun.com/api/auth then do `{ctx.prefix}verify <apiKey>` in my DMs or anywhere in this server. \nBe careful who you share this key with. To learn more check out https://github.com/speedruncomorg/api/blob/master/authentication.md"
                )
                return
        if ctx.guild != None:
            await ctx.message.delete()
        async with ctx.typing():
            if userID == None:
                userID = ctx.message.author.id
            await verifyNew(self, apiKey, userID)

    @commands.command()
    async def verified(self, ctx, modName=None):
        async with ctx.typing():
            if modName is None:
                await ctx.send("Please supply a moderator to view stats of")
                return
            await verifiedCount(self, ctx, modName)

    @tasks.loop(minutes=10.0)
    async def checker(self):
        data = json.loads(Path("./api_keys.json").read_text())
        for key, value in data.items():
            try:
                await verifyNew(self, None, key)
            except Exception as e:
                print(f"{key}: {value}")
                print(e.args)
                continue


async def setup(bot):
    await bot.add_cog(Src(bot))
