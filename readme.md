# Minecraft Bedrock Discord Bot

## How to
Make a file called `config.json` and add
```json
{
	"token": "your_bot_token"
}
```

Launch the bot with `python3 main.py` and you're ready to go. Unless dependencies. Dependencies are google cloud and discord.

Install the dependencies with `python -m pip install -r requirements.txt`

A few "dangerous" commands such as `!purge` are restriced to `bot_masters`, to add a bot master add it to `config.json`. Example:
```json
{
	"token": "your_bot_token",
	"bot_masters": <users_discord_id>
}
```
You can also use lists, for example: `"bot_masters": [280428276810383370, 99457716614885376]`

A user added as a botmaster will be able to edit the config via discord with the command `!setvar <var_name> <var_value>`  
`!setvar` also supports lists which can be added like so: `!setvar <var_name> [<index 0>, <index 1>]`

This bot was built as a fork of [celesteBot](https://github.com/CelesteClassic/celestebot), so a lot of code is recycled.  
Feel free to make a pull request or use the code here.
