import io
import re
from tabulate import tabulate
import telebot
from loguru import logger

import config
import wg_utils
from db import SessionLocal
from crud import user as db_user
from crud import wg_user as db_wg_user


wga_db = SessionLocal()

bot = telebot.TeleBot(config.BOT_API_TOKEN)


@bot.message_handler(commands=["help", "start"])
def send_help(message):
    help_message = """
        Available comands:
        /get_users: show active users
        /add_user: add new user
        /remove_user: remove existing user
        /about_me: show your profile
        /help: show this message
    """
    bot.reply_to(message, help_message)


@bot.message_handler(commands="get_users")
def get_user_list(message):
    username = message.from_user.username
    if db_user.get_role_by_name(wga_db, username) == "admin":
        wg_user_list = db_wg_user.get_wguser_list(wga_db)
        if len(wg_user_list) > 0:
            user_table = []
            th = ['Username', 'Creation date']
            for wg_user in wg_user_list:
                row = (
                    wg_user.name,
                    wg_user.creation_date.strftime("%d.%m.%Y %H:%M:%S")
                )
                user_table.append(row)
            msg = (
                "<pre>"
                f"{tabulate(user_table, headers=th)}"
                "</pre>"
            )
            bot.send_message(
                message.chat.id,
                msg,
                parse_mode='HTML'
            )
        else:
            bot.send_message(
                message.chat.id,
                "No users found in database"
            )
    else:
        bot.send_message(
            message.chat.id,
            "You do not have sufficient privileges"
        )


@bot.message_handler(commands=["add_user"])
def send_add_user(message):
    username = message.from_user.username
    if db_user.get_role_by_name(wga_db, username) == "admin":
        msg = bot.reply_to(
            message,
            "Write username to add:"
        )
        bot.register_next_step_handler(msg, add_user)
    else:
        bot.send_message(
            message.chat.id,
            "You do not have sufficient privileges"
        )


def add_user(message):
    if not re.match(r"^[0-9a-z_]{3,10}$", message.text):
        bot.send_message(
            message.chat.id,
            (
                "User name must contain only "
                "lowercase letters, digits and '_' character. "
                "Min lenght: 3. Max lenght: 10"
            )
        )
    else:
        if not db_wg_user.get_wguser_by_name(wga_db, message.text):
            wg_user = wg_utils.get_wg_user(wga_db, message.text)
            create_wg_user = db_wg_user.create_wguser(wga_db, wg_user)
            creation_date = create_wg_user.creation_date.strftime(
                "%d.%m.%Y %H:%M:%S"
            )
            msg = (
                f"User {create_wg_user.name} "
                f"created at {creation_date}"
            )
            logger.debug(msg)
            bot.send_message(message.chat.id, msg)

            f = io.StringIO(wg_utils.get_user_config(wg_user))
            bot.send_document(
                message.chat.id,
                f,
                visible_file_name=f"{wg_user.name}.conf"
            )
        else:
            bot.send_message(
                message.chat.id,
                "User already exist"
            )


@bot.message_handler(commands=["remove_user"])
def send_remove_user(message):
    username = message.from_user.username
    if db_user.get_role_by_name(wga_db, username) == "admin":
        msg = bot.reply_to(
            message,
            "Write username to delete:"
        )
        bot.register_next_step_handler(msg, remove_user)
    else:
        bot.send_message(
            message.chat.id,
            "You do not have sufficient privileges"
        )


def remove_user(message):
    if not re.match(r"^[0-9a-z_]{3,10}$", message.text):
        bot.send_message(
            message.chat.id,
            (
                "User name must contain only "
                "lowercase letters, digits and '_' character. "
                "Min lenght: 3. Max lenght: 10"
            )
        )
    else:
        if db_wg_user.get_wguser_by_name(wga_db, message.text):
            wg_utils.remove_wg_user(wga_db, message.text)
            msg = (f"User {message.text} removed")
            logger.debug(msg)
            bot.send_message(message.chat.id, msg)
        else:
            bot.send_message(
                message.chat.id,
                "User with this name not exist"
            )


@bot.message_handler(commands=["about_me"])
def get_my_profile(message):
    username = message.from_user.username
    wga_user = db_user.get_user_by_name(wga_db, username)
    if wga_user:
        bot.send_message(message.chat.id, f"Your role: {wga_user.role}")
    else:
        bot.send_message(message.chat.id, "You are not added to the database")


@bot.message_handler(content_types=["text"])
def main_message(message):
    send_help(message)
