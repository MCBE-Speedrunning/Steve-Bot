from discord.ext import commands


class Errorhandler(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

	@commands.Cog.listener()
	async def on_command_error(self, ctx, error):
		if isinstance(error, commands.CommandNotFound):
			return

		if isinstance(error, commands.CommandOnCooldown):
			return

		raise error


def setup(bot):
	bot.add_cog(Errorhandler(bot))
