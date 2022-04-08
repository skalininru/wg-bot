import os

LOG_LEVEL = os.getenv("WGA_LOG_LEVEL", "INFO")

BOT_API_TOKEN = os.getenv("BOT_API_TOKEN")

DB_HOST = os.getenv("WGA_DB_HOST")
DB_NAME = os.getenv("WGA_DB_NAME")
DB_USER = os.getenv("WGA_DB_USER")
DB_PASSWORD = os.getenv("WGA_DB_PASSWORD")

SERVER_PUBLIC_KEY = os.getenv("WG_SERVER_PUBLIC_KEY")
SERVER_DNS = os.getenv("WG_SERVER_DNS", "1.1.1.1")
SERVER_ENDPOINT = os.getenv("WG_SERVER_ENDPOINT")
SERVER_INTERFACE = os.getenv("WG_SERVER_INTERFACE", "wg0")
SERVER_NETWORK = os.getenv("WG_SERVER_NETWORK", "10.0.0.0/24")
