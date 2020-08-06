import asyncio
import json
from bot import ziBot

def check_jsons():
    try:
        f = open('config.json', 'r')
    except FileNotFoundError:
        token = input('Enter your bot\'s token: ')
        with open('config.json', 'w+') as f:
            json.dump({"token": token}, f, indent=4)

def init_bot():
    bot = ziBot()
    with open('config.json', 'r') as f:
        data=json.load(f)
    bot.remove_command('help')
    bot.run()

if __name__ == "__main__":
    check_jsons()
    init_bot()
