import asyncio
import json
import logging

from bot import BedrockBot
from colorama import init as init_colorama


def check_jsons():
    try:
        f = open("config.json", "r")
    except FileNotFoundError:
        token = input("BOT SETUP - Enter bot token: ")
        with open("config.json", "w+") as f:
            json.dump({"token": token}, f, indent=4)

    try:
        f = open("blacklist.json", "r")
    except FileNotFoundError:
        with open("blacklist.json", "w+") as f:
            json.dump([], f, indent=4)

    try:
        f = open("runs_blacklist.json", "r")
    except FileNotFoundError:
        with open("runs_blacklist.json", "w+") as f:
            json.dump({"videos": [], "players": []}, f, indent=4)


def setup_logging():
    FORMAT = "%(asctime)s - [%(levelname)s]: %(message)s"
    DATE_FORMAT = "%d/%m/%Y (%H:%M:%S)"

    logger = logging.getLogger("discord")
    logger.setLevel(logging.INFO)

    file_handler = logging.FileHandler(
        filename="discord.log", mode="a", encoding="utf-8"
    )
    file_handler.setFormatter(logging.Formatter(fmt=FORMAT, datefmt=DATE_FORMAT))
    file_handler.setLevel(logging.INFO)
    logger.addHandler(file_handler)

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(logging.Formatter(fmt=FORMAT, datefmt=DATE_FORMAT))
    console_handler.setLevel(logging.WARNING)
    logger.addHandler(console_handler)


def run_bot():

    bot = BedrockBot()
    bot.run()


if __name__ == "__main__":

    init_colorama(autoreset=True)

    setup_logging()

    check_jsons()

    run_bot()
