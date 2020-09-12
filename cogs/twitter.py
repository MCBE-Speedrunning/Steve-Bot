import json

import discord
import requests
import tweepy
from discord.ext import commands, tasks


class StreamListener(tweepy.StreamListener):
    def __init__(self):
        with open("./config.json") as f:
            self.config = json.load(f)

    def on_error(self, status_code):
        if status_code == 420:
            print("Rate limit reached. ")
            # returning False in on_error disconnects the stream
            return False

    def on_data(self, data):
        data = json.loads(data)
        try:
            tweetUser = data["tweet"]["user"]["screen_name"]
            tweetID = data["tweet"]["id_str"]
        except:
            tweetUser = data["user"]["screen_name"]
            tweetID = data["id_str"]
        tweetLink = f"https://twitter.com/{tweetUser}/status/{tweetID}"
        body = {"content": tweetLink}
        global config
        r = requests.post(
            self.config["574267523869179904"]["tweetWebhook"],
            headers={"Content-Type": "application/json"},
            data=json.dumps(body),
        )  # config['574267523869179904']['tweetWebhook'], data=json.dumps(body))
        print(r.status_code)
        print(r.text)
        # print(json.dumps(data, indent='\t'))


class Twitter(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        auth = tweepy.OAuthHandler(
            self.bot.config["twitter"]["consumer_key"],
            self.bot.config["twitter"]["consumer_secret"],
        )
        auth.set_access_token(
            self.bot.config["twitter"]["access_token"],
            self.bot.config["twitter"]["access_token_secret"],
        )

        api = tweepy.API(auth)
        myStreamListener = StreamListener()
        stream = tweepy.Stream(auth=api.auth, listener=myStreamListener)
        stream.filter(follow=["1287799985040437254"], is_async=True)


def setup(bot):
    bot.add_cog(Twitter(bot))
