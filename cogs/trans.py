import discord
import six
from discord.ext import commands
from google.cloud import translate_v2 as translate

translate_client = translate.Client()


async def translateMsg(text: str, target: str = "en") -> str:
    # Text can also be a sequence of strings, in which case this method
    # will return a sequence of results for each text.
    if isinstance(text, six.binary_type):
        text = text.decode("utf-8")
    result = translate_client.translate(text, target_language=target)
    print("Text: {}".format(result["input"]))
    print("Translation: {}".format(result["translatedText"]))
    print("Detected source language: {}".format(result["detectedSourceLanguage"]))
    result["translatedText"] = result["translatedText"].replace("&lt;", "<")
    result["translatedText"] = result["translatedText"].replace("&gt;", ">")
    result["translatedText"] = result["translatedText"].replace("&#39;", "'")
    result["translatedText"] = result["translatedText"].replace("&quot;", '"')
    result["translatedText"] = result["translatedText"].replace("<@! ", "<@!")
    result["translatedText"] = result["translatedText"].replace("<@ ", "<@")
    result["translatedText"] = result["translatedText"].replace("<# ", "<#")
    return result


class Trans(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(
        help="Translate text in english (using google translate)",
        brief="Translate to english",
        aliases=["翻译", "脑热", "动漫"],
    )
    async def translate(self, ctx, *, message):
        """Translate to english"""
        response = await translateMsg(message)
        embed = discord.Embed(
            title="Translation",
            description=f"{ctx.message.author.mention} says:",
            timestamp=ctx.message.created_at,
            color=0x4D9AFF,
        )
        embed.add_field(
            name=f"[{response['detectedSourceLanguage']}] Source:",
            value=response["input"],
            inline=False,
        )
        embed.add_field(
            name="Translation", value=response["translatedText"], inline=True
        )
        await ctx.send(embed=embed)

    @commands.command()
    async def trans(self, ctx, lan, *, message):
        """Translate to a specific language"""
        response = await translateMsg(message, lan)
        embed = discord.Embed(
            title="Translation",
            description=f"{ctx.message.author.mention} says:",
            timestamp=ctx.message.created_at,
            color=0x4D9AFF,
        )
        embed.add_field(
            name=f"[{response['detectedSourceLanguage']}] Source:",
            value=response["input"],
            inline=False,
        )
        embed.add_field(
            name="Translation", value=response["translatedText"], inline=True
        )
        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Trans(bot))
