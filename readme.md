# Minecraft Bedrock Discord Bot

## How to
Launch the bot with `python3 main.py` and you're ready to go. Unless dependencies. Dependencies are google cloud and discord.

Install the dependencies with `python -m pip install -r requirements.txt`

A few "dangerous" commands such as `!purge` are restriced to `bot_masters`, to add a bot master add it to `config.json`. Example:
```json
{
	"token": "your_bot_token",
    "<guild_id>": {
	    "bot_masters": <users_discord_id>
    }
}
```
`guild_id` is the ID of the discord server in the form of a string while user IDs are integers

You can also use lists, for example: `"bot_masters": [280428276810383370, 99457716614885376]`

A user added as a botmaster will be able to edit the config via discord with the command `!setvar <var_name> <var_value>`
`!setvar` also supports lists which can be added like so: `!setvar <var_name> [<index 0>, <index 1>]`

This bot was built as a fork of [celesteBot](https://github.com/CelesteClassic/celestebot), so a lot of code is recycled.
Feel free to make a pull request or use the code here.
