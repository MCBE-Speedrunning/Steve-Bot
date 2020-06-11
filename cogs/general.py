from discord.ext import commands
import discord
import datetime

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

		# Very very shit 
		"""
		await ctx.send(str(user.avatar_url))
		request.urlretrieve(str(user.avatar_url), "temp.webp")
		#filename = wget.download(user.avatar_url, out="temp.webp")
		image = Image.open("temp.webp").convert("RGB")
		image.save("temp.png", "PNG")
		
		f = discord.File("temp.png", filename="temp.png")
		#await messagable.send(file=f, embed=e)
		"""
		output = ""
		for i in user.roles:
			output += i.mention

		if user.color.value == 0:
			color = 16777210
		else:
			color = user.color

		embed=discord.Embed(title=user.name, description=user.mention, color=color, timestamp=ctx.message.created_at)
		#embed.set_thumbnail(url="attachment://temp.webp")
		embed.set_thumbnail(url=user.avatar_url)
		embed.set_image(url="attachment://temp.png")
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
		elif type(user)=="str":
			user = self.bot.get_user(int(user))

		coop_role = ctx.guild.get_role(694261282861219952)

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
		#embed.set_thumbnail(url="attachment://temp.webp")
		embed.set_thumbnail(url=guild.icon_url)
		embed.set_image(url=guild.splash_url)
		embed.add_field(name="Created on", value=guild.created_at.date(), inline=True)
		embed.add_field(name="Members", value=guild.member_count, inline=True)
		embed.add_field(name="Emojis", value=emojiList, inline=True)
		embed.add_field(name="Owner", value=guild.owner.mention, inline=True)
		embed.set_footer(text=f"ID: {guild.id}")
		await ctx.send(embed=embed)

def setup(bot):
	bot.add_cog(General(bot))
