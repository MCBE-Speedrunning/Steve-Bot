import json
from discord.ext import commands, tasks
import discord
import tweepy
import asyncio

class StreamListener(tweepy.StreamListener):
	def on_error(self, status_code):
		if status_code == 420:
			print("Rate limit reached. ")
			#returning False in on_error disconnects the stream
			return False

	def on_data(self, data):
		global channelTweet
		data = json.loads(data)
		tweetUser = data['user']['screen_name']
		tweetID = data['id_str']
		tweetLink = f'https://twitter.com/{tweetUser}/status/{tweetID}'
		loop = asyncio.get_event_loop()
		try:
			loop.run_until_complete(channelTweet.send(tweetLink))
		finally:
			loop.run_until_complete(loop.shutdown_asyncgens())
			loop.close()
		#print(json.dumps(data, indent='\t'))


class Twitter(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

		global channelTweet
		channelTweet = self.bot.get_channel(737713121447378965)

		auth = tweepy.OAuthHandler(self.bot.config['twitter']['consumer_key'], self.bot.config['twitter']['consumer_secret'])
		auth.set_access_token(self.bot.config['twitter']['access_token'], self.bot.config['twitter']['access_token_secret'])

		api = tweepy.API(auth)
		myStreamListener = StreamListener()
		stream = tweepy.Stream(auth = api.auth, listener=myStreamListener)
		stream.filter(follow=['1287799985040437254'], is_async=True)

def setup(bot):
	bot.add_cog(Twitter(bot))