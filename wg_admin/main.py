from loguru import logger

import config
from db import engine
from wg_bot.bot import bot


logger.info(f"Log level is set to: {config.LOG_LEVEL}")
logger.debug(
    "Database config: "
    f"db_host: {config.DB_HOST}, "
    f"db_name: {config.DB_NAME}, "
    f"db_user: {config.DB_USER}"
)

try:
    engine.connect()
    engine.execute("select 1")
    logger.info("Database succesfully connected")
except Exception as db_except:
    logger.error("An error occured when attemting to connect to database")
    raise db_except


bot.infinity_polling()
