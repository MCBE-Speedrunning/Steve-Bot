from discord.ext import commands
import discord


class Logs(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

	@commands.Cog.listener()
	async def on_message_delete(self, message):
		if (message.id in self.bot.messageBlacklist):
			self.bot.messageBlacklist.remove(message.id)
			return
		if message.guild.id != 574267523869179904:
			return 
		if message.author.color.value == 0:
			color = 16777210
		else:
			color = message.author.color
		channel = self.bot.get_channel(int(self.bot.config[str(message.guild.id)]["logs_channel"]))
		embed = discord.Embed(
			title='Deleted Message',
			color=color,
			timestamp=message.created_at
		)
		embed.add_field(
			name='User', value=message.author.mention, inline=True)
		embed.add_field(
			name='Channel', value=message.channel.mention, inline=True)
		embed.add_field(name='Message', value=message.content, inline=False)
		await channel.send(embed=embed)

	@commands.Cog.listener()
	async def on_message_edit(self, before, after):
		if after.guild.id != 574267523869179904:
			return 
		channel = self.bot.get_channel(int(self.bot.config[str(before.guild.id)]["logs_channel"]))
		if before.author.color.value == 0:
			color = 16777210
		else:
			color = before.author.color
		embed = discord.Embed(
			title='Edited Message',
			color=color,
			timestamp=after.edited_at
		)
		embed.add_field(
			name='User', value=before.author.mention, inline=True)
		embed.add_field(
			name='Channel', value=before.channel.mention, inline=True)
		embed.add_field(name='Original Message',
						value=before.content, inline=False)
		embed.add_field(name='New Message', value=after.content, inline=False)
		await channel.send(embed=embed)


def setup(bot):
	bot.add_cog(Logs(bot))
