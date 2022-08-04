import os

from loguru import logger

required_variables = [
    "BOT_API_TOKEN",
    "WGA_DB_PASSWORD",
    "WG_SERVER_PUBLIC_KEY",
    "WG_SERVER_ENDPOINT",
    "WG_ADMIN_USER"
]

LOG_LEVEL = os.getenv("WGA_LOG_LEVEL", "INFO")
logger.debug("Init and check config")

for var in required_variables:
    if var not in os.environ:
        err_message = (
            "One or more requiered env variable is missing\n"
            "Required variables:\n"
            f"{required_variables}"
        )
        raise ValueError(err_message)
logger.debug("Configuration initialized successfully")

BOT_API_TOKEN = os.getenv("BOT_API_TOKEN")

DB_HOST = os.getenv("WGA_DB_HOST", "127.0.0.1")
DB_NAME = os.getenv("WGA_DB_NAME", "wga")
DB_USER = os.getenv("WGA_DB_USER", "u_wga")
DB_PASSWORD = os.getenv("WGA_DB_PASSWORD")

ADMIN_USER = os.getenv("WG_ADMIN_USER")

SERVER_PUBLIC_KEY = os.getenv("WG_SERVER_PUBLIC_KEY")
SERVER_DNS = os.getenv("WG_SERVER_DNS", "1.1.1.1")
SERVER_ENDPOINT = os.getenv("WG_SERVER_ENDPOINT")
SERVER_INTERFACE = os.getenv("WG_SERVER_INTERFACE", "wg0")
SERVER_NETWORK = os.getenv("WG_SERVER_NETWORK", "10.0.0.0/24")
