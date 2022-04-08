from telebot import types


start_kb = types.InlineKeyboardMarkup()

key_get_user_list = types.InlineKeyboardButton(
    text="Get user list",
    callback_data="user_list"
)
start_kb.add(key_get_user_list)

key_add_user = types.InlineKeyboardButton(
    text="Add user",
    callback_data="add_user"
)
start_kb.add(key_add_user)

key_me = types.InlineKeyboardButton(
    text="Get my profile",
    callback_data="my_profile"
)
start_kb.add(key_me)


fr = types.ForceReply()
