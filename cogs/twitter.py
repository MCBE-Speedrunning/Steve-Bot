from discord.ext import commands, tasks
import discord
import tweepy

class MyStreamListener(tweepy.StreamListener):
	def on_error(self, status_code):
		if status_code == 420:
			#returning False in on_error disconnects the stream
			return False

	def on_status(self, status):
		if hasattr(status, "retweeted_status"):  # Check if Retweet
			try:
				print(status.retweeted_status.extended_tweet["full_text"])
			except AttributeError:
				print(status.retweeted_status.text)
		else:
			try:
				print(status.extended_tweet["full_text"])
			except AttributeError:
				print(status.text)


class Twitter(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

		auth = tweepy.OAuthHandler(self.bot.config['twitter']['consumer_key'], self.bot.config['twitter']['consumer_secret'])
		auth.set_access_token(self.bot.config['twitter']['access_token'], self.bot.config['twitter']['access_token_secret'])

		api = tweepy.API(auth)
		myStreamListener = MyStreamListener()
		self.myStream = tweepy.Stream(auth = api.auth, listener=myStreamListener)
		self.myStream.filter(follow=['1287799985040437254'], is_async=True)

def setup(bot):
	bot.add_cog(Twitter(bot))