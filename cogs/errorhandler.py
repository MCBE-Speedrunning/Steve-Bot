from discord.ext import commands


class Errorhandler(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

	@commands.Cog.listener()
	async def on_command_error(self, ctx, error):
		if isinstance(error, commands.CommandNotFound):
			return

		if isinstance(error, commands.CommandOnCooldown):
			return await ctx.send(f'{ctx.author.mention}, you have to wait {round(error.retry_after, 2)} seconds before using this again')

		raise error


def setup(bot):
	bot.add_cog(Errorhandler(bot))
