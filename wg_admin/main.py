from loguru import logger

import config
from db import engine, SessionLocal
from wg_bot.bot import bot
from crud import user as db_user


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

wga_db = SessionLocal()

if not db_user.get_user_by_name(wga_db, config.ADMIN_USER):
    admin_user = db_user.create_admin_user(wga_db, config.ADMIN_USER)
    logger.debug(f"Added admin user {admin_user.name} with id {admin_user.id}")
else:
    logger.debug("Admin user already exist")

bot.infinity_polling()
