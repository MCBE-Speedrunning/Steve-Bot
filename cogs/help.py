from discord.ext import commands
from random import randint

class MyHelpCommand(commands.MinimalHelpCommand):
	messages = ["...!", ".party()!", "<PLAYERNAME> IS YOU",
		"10 years of Mining and Crafting!",
		"12 herbs and spices!",
		"12345 is a bad password!",
		"150 bpm for 400000 minutes!",
		"20 GOTO 10!",
	    "~~4815162342~~ 5 at most lines of code!",
	    "90210!",
	    "A skeleton popped out!",
	    "Absolutely fixed relatively broken coordinates",
	    "Absolutely no memes!",
	    "Afraid of the big, black bat!",
	    "Age of Wonders is better!",
	    "Ahhhhhh!"]
	aliases_heading = "Other options: "
	def get_command_signature(self, command):
		return f'``{self.clean_prefix}{command.qualified_name} {command.signature}``'
	def get_ending_note(self):
		return self.messages[randint(0, len(self.messages)-1)]

class Help(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
		self._original_help_command = bot.help_command
		bot.help_command = MyHelpCommand()
		bot.help_command.cog = self

	def cog_unload(self):
		self.bot.help_command = self._original_help_command


def setup(bot):
	bot.add_cog(Help(bot))
