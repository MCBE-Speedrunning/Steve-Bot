from discord.ext import commands
import discord
import datetime
import requests
import json

def dump(obj):
	output = ""
	for attr in dir(obj):
		output += "\nobj.%s = %r" % (attr, getattr(obj, attr))
		print("obj.%s = %r" % (attr, getattr(obj, attr)))
	return output


class General(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

	@commands.command()
	async def userinfo(self, ctx, user: discord.Member=None):
		#await ctx.send(f"```py\n{dump(user)}```")

		if not user:
			user = ctx.message.author

		output = ""
		for i in user.roles:
			output += i.mention + " "

		if user.color.value == 0:
			color = 16777210
		else:
			color = user.color

		embed=discord.Embed(title=user.name, description=user.mention, color=color, timestamp=ctx.message.created_at)
		#embed.set_thumbnail(url="attachment://temp.webp")
		embed.set_thumbnail(url=user.avatar_url_as(format="png"))
		embed.add_field(name="Nickname", value=user.display_name, inline=False)
		embed.add_field(name="Joined on", value=user.joined_at.date(), inline=True)
		embed.add_field(name="Status", value=user.status, inline=True)
		embed.add_field(name="Created account on", value=user.created_at.date(), inline=True)
		embed.add_field(name="Roles", value=output, inline=True)
		embed.set_footer(text=f"ID: {user.id}")
		await ctx.send(embed=embed)
		#os.remove("temp.webp")
		#os.remove("temp.png")

	@commands.command()
	async def coop(self, ctx, *, user: discord.Member=None):
		if not user:
			user = ctx.message.author
		else:
			user = self.bot.get_user(int(user))

		coop_role = ctx.guild.get_role(int(self.bot.config[str(ctx.message.guild.id)]["coop_roleID"]))

		if coop_role in user.roles:
			await user.remove_roles(coop_role)
			await ctx.send('You have left coop gang')
		else:
			await user.add_roles(coop_role)
			await ctx.send("You are now in the coop gang")

	@commands.command()
	async def serverinfo(self, ctx, guild=None):
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

		embed=discord.Embed(title=guild.name, description=guild.description, color=color, timestamp=ctx.message.created_at)
		embed.set_thumbnail(url=guild.icon_url_as(format="png"))
		embed.set_image(url=guild.splash_url_as(format="png"))
		embed.add_field(name="Created on", value=guild.created_at.date(), inline=True)
		embed.add_field(name="Members", value=guild.member_count, inline=True)
		embed.add_field(name="Emojis", value=emojiList, inline=True)
		embed.add_field(name="Owner", value=guild.owner.mention, inline=True)
		embed.set_footer(text=f"ID: {guild.id}")
		await ctx.send(embed=embed)

	@commands.command()
	async def xboxUser(self, ctx, *, gamertag=None):
		if not gamertag:
			await ctx.send("You need to specify a gamer, gamer")
			return

		r = requests.get(f"https://xbl-api.prouser123.me/profile/gamertag/{gamertag}")
		gamer = json.loads(r.text)

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
				Gamerscore = i["value"]+"<:gamerscore:727131234534424586>"
				continue
			if i["id"] == "AccountTier":
				accountTier = i["value"]
				continue
			if i["id"] == "XboxOneRep":
				reputation = i["value"]
				continue
			if i["id"] == "PreferredColor":
				color = int(json.loads(requests.get(i["value"]).text)["primaryColor"], 16)
				continue
			if i["id"] == "Location":
				location = i["value"]
				continue
			if i["id"] == "Bio":
				#if len(i["value"]) == 0:
				#	Bio = "Unknown"
				#else:
				Bio = i["value"]
				continue
			if i["id"] == "Watermarks":
				Watermarks = i["value"]
				continue
			if i["id"] == "RealName":
				RealName = i["value"]
				continue


		embed=discord.Embed(title=gameName, description=Bio, color=color, timestamp=ctx.message.created_at)
		embed.set_thumbnail(url=picUrl)
		embed.add_field(name="Gamerscore", value=Gamerscore, inline=True)
		if len(location) != 0:
			embed.add_field(name="Location", value=location, inline=True)
		if len(Watermarks) != 0:
			embed.add_field(name="Watermarks", value=Watermarks, inline=True)
		embed.add_field(name="Account Tier", value=accountTier, inline=True)
		embed.add_field(name="Reputation", value=reputation, inline=True)
		await ctx.send(embed=embed)

def setup(bot):
	bot.add_cog(General(bot))
