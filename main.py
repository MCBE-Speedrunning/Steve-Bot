import asyncio
import logging

from colorama import init as init_colorama

from bot import CelesteBot


def setup_logging():
    FORMAT = '%(asctime)s - [%(levelname)s]: %(message)s'
    DATE_FORMAT = '%d/%m/%Y (%H:%M:%S)'

    logger = logging.getLogger('discord')
    logger.setLevel(logging.INFO)

    file_handler = logging.FileHandler(filename='discord.log', mode='a', encoding='utf-8')
    file_handler.setFormatter(logging.Formatter(fmt=FORMAT, datefmt=DATE_FORMAT))
    file_handler.setLevel(logging.INFO)
    logger.addHandler(file_handler)

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(logging.Formatter(fmt=FORMAT, datefmt=DATE_FORMAT))
    console_handler.setLevel(logging.WARNING)
    logger.addHandler(console_handler)

def run_bot():

    bot = CelesteBot()
    bot.run()

if __name__ == "__main__":
    
    init_colorama(autoreset=True)

    setup_logging()
    
    run_bot()
