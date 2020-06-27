from discord.ext import commands
import discord
from google.cloud import translate_v2 as translate
import six
translate_client = translate.Client()

async def translateMsg(text, target="en"):
	# Text can also be a sequence of strings, in which case this method
	# will return a sequence of results for each text.
	if isinstance(text, six.binary_type):
		text = text.decode('utf-8')
	result = translate_client.translate(
		text, target_language=target)
	print(u'Text: {}'.format(result['input']))
	print(u'Translation: {}'.format(result['translatedText']))
	print(u'Detected source language: {}'.format(
		result['detectedSourceLanguage']))
	result['translatedText'] = result['translatedText'].replace("&lt;", "<")
	result['translatedText'] = result['translatedText'].replace("&gt;", ">")
	result['translatedText'] = result['translatedText'].replace("&#39;", "'")
	result['translatedText'] = result['translatedText'].replace("&quot;", '"')
	result['translatedText'] = result['translatedText'].replace("<@! ", "<@!")
	result['translatedText'] = result['translatedText'].replace("<@ ", "<@")
	result['translatedText'] = result['translatedText'].replace("<# ", "<#")
	return result;

class Trans(commands.Cog):

	def __init__(self, bot):
		self.bot = bot

	@commands.command(help="Translate text in english (using google translate)", brief="Translate to english", aliases=["翻译", "脑热", "动漫"])
	async def translate(self, ctx, *, message):
		response = await translateMsg(message)
		embed=discord.Embed(title="Translation",description=f"{ctx.message.author.mention} says:", timestamp=ctx.message.created_at, color=0x4d9aff)
		embed.add_field(name=f"[{response['detectedSourceLanguage']}] Source:" , value=response['input'], inline=False)
		embed.add_field(name="Translation", value=response['translatedText'], inline=True)
		await ctx.send(embed=embed)

	@commands.command()
	async def trans(self, ctx, lan, *, message):
		response = await translateMsg(message, lan)
		embed=discord.Embed(title="Translation",description=f"{ctx.message.author.mention} says:", timestamp=ctx.message.created_at, color=0x4d9aff)
		embed.add_field(name=f"[{response['detectedSourceLanguage']}] Source:" , value=response['input'], inline=False)
		embed.add_field(name="Translation", value=response['translatedText'], inline=True)
		await ctx.send(embed=embed)

def setup(bot):
	bot.add_cog(Trans(bot))
