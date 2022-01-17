import asyncio
from os import mkdir
from pathlib import Path

import yaml
from loguru import logger
from databases import Database
from sqlalchemy import MetaData, create_engine
from aiogram import Dispatcher, Bot
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from objects import globals

DEBUG_PATH = CONFIG_PATH = DB_PATH = Path(__file__).resolve().parent
DEBUG_DIRNAME = r"%s/debug" % DEBUG_PATH

async def main():
    # Config
    if not Path(r"%s/config.yaml" % CONFIG_PATH).parent.exists():
        logger.error("Don't exists file is 'config.yaml")
    else:
        with open(r"%s/config.yaml" % CONFIG_PATH) as f:
            config = yaml.load(f, Loader=yaml.FullLoader)
            globals.config = config
    
    # Debug
    if not Path(DEBUG_DIRNAME ).exists():
        mkdir(DEBUG_DIRNAME )
    logger.add(
        r"%s/debug.log" % DEBUG_DIRNAME, format="{time} {level} {message}",
        level="DEBUG", rotation="1 week",
        compression="zip")

    globals.db = Database(r"sqlite:///%s/db.sqlite3" % DB_PATH)
    globals.metadata = MetaData()

    globals.bot = Bot(token=globals.config["BOT_TOKEN"], parse_mode="HTML")
    globals.dp = Dispatcher(globals.bot, storage=MemoryStorage())

    bot_info: dict = await globals.bot.get_me()
    logger.info(f"Bot username: @{bot_info.username}. Bot Id: {bot_info.id}")

    import commands

    await globals.dp.start_polling()

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(main())
    except KeyboardInterrupt:
        logger.info("Bot stopped")