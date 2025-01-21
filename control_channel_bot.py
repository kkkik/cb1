import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
bT = '7617721774:AAGtGSsUz4CeTwRXrt_yRmpf1Upvr0HJTiM' #[Bot Token]
bot = telebot.TeleBot(bT)
CHANNELS = ['@username1', '@username2']  #[Channals UserNames and bot must be admin in the channels], accepts up to 50channel.
current_channel = None # [Current Channal]
last_message_id = None #[ Saving last message id]
@bot.message_handler(commands=['start'])
def start_message(message):
    bot.reply_to(
        message,
        "— Hi sir, I'm a bot to help you manage your channels.", #Start messege
        reply_markup=select_channel_menu()
    )#yepaki_dev
# [Choose Channal method]
def select_channel_menu():
    markup = InlineKeyboardMarkup()
    for channel in CHANNELS:
        markup.add(InlineKeyboardButton(f"• Select {channel}", callback_data=f"select_{channel}"))
    return markup
#[ Main menu after choosing the channeal ]
def main_menu():
    markup = InlineKeyboardMarkup()
    markup.row_width = 2
    markup.add(#yepaki_dev
        InlineKeyboardButton("• New Post.", callback_data="post_message"),
        InlineKeyboardButton("• Delete LastMessage.", callback_data="delete_last_message"),
        InlineKeyboardButton("• Pin LastMessage.", callback_data="pin_last_message"),
        InlineKeyboardButton("• Change Channel Name.", callback_data="change_channel_name"),
        InlineKeyboardButton("• Change Channel Photo.", callback_data="change_channel_photo"),
        InlineKeyboardButton("• Change Channel Description.", callback_data="change_channel_description")
    )
    return markup
# [ post a message method]
def post_new_message(chat_id):
    msg = bot.send_message(chat_id, f"• Send the message you want to post in {current_channel}.")
    bot.register_next_step_handler(msg, publish_message)

def publish_message(message):
    global last_message_id
    try:
        sent_msg = bot.send_message(current_channel, message.text)
        last_message_id = sent_msg.message_id
        bot.reply_to(message, "• Posted Done ✅.")
    except Exception as e:
        bot.reply_to(message, f"• Error: {e}❎")
#[ Del last message using Message id (last_message_id) ]
def delete_last_message(chat_id):
    global last_message_id
    if last_message_id:
        try:#yepaki_dev
            bot.delete_message(current_channel, last_message_id)
            bot.send_message(chat_id, "• Last message has been deleted.")
            last_message_id = None
        except Exception as e:
            bot.send_message(chat_id, f"• Error: {e}")
    else:
        bot.send_message(chat_id, "• No message to delete.")

#[ pin the last message ]
def pin_last_message(chat_id):
    global last_message_id
    if last_message_id:
        try:
            bot.pin_chat_message(current_channel, last_message_id)
            bot.send_message(chat_id, "• Last message has been pinned ✅.")
        except Exception as e:
            bot.send_message(chat_id, f"• Error: {e}")
    else:#yepaki_dev
        bot.send_message(chat_id, "• No message to pin.")

#[ Change channal name func]
def change_channel_name(chat_id):
    msg = bot.send_message(chat_id, "• Send new channel name:")
    bot.register_next_step_handler(msg, update_channel_name)

def update_channel_name(message):
    try:#yepaki_dev
        new_name = message.text
        bot.set_chat_title(current_channel, new_name)
        bot.reply_to(message, f"• Successfully changed to: {new_name} ✅")
    except Exception as e:
        bot.reply_to(message, f"• Error: {e}")

"""[Change channal photo (Must be 720x720 or 1080x1080)](not important)"""
def change_channel_photo(chat_id):
    msg = bot.send_message(chat_id, "• Send the photo you want to set as channel photo:")
    bot.register_next_step_handler(msg, update_channel_photo)

def update_channel_photo(message):
    try:#yepaki_dev
        if message.photo:
            file_info = bot.get_file(message.photo[-1].file_id)
            downloaded_file = bot.download_file(file_info.file_path)
            with open("channel_photo.jpg", "wb") as new_file:
                new_file.write(downloaded_file)

            with open("channel_photo.jpg", "rb") as photo:
                bot.set_chat_photo(current_channel, photo)

            bot.reply_to(message, "• Channel photo updated successfully ✅.")
        else:
            bot.reply_to(message, "• Please send a valid photo.")
    except Exception as e:
        bot.reply_to(message, f"• Error: {e}")
#[ change channal bio]
def change_channel_description(chat_id):
    msg = bot.send_message(chat_id, "• Send new channel description:")
    bot.register_next_step_handler(msg, update_channel_description)

def update_channel_description(message):
    try:#yepaki_dev
        new_description = message.text
        bot.set_chat_description(current_channel, new_description)
        bot.reply_to(message, f"• Description updated successfully ✅.")
    except Exception as e:
        bot.reply_to(message, f"• Error: {e}")

# [Buttons services( Dont Change AnyThing )]
@bot.callback_query_handler(func=lambda call: True)
def handle_callback(call):
    global current_channel
    if call.data.startswith("select_"):
        current_channel = call.data.split("_", 1)[1]
        bot.edit_message_text(
            f"— You are now managing {current_channel}.",
            call.message.chat.id,
            call.message.message_id,
            reply_markup=main_menu()
        )
    elif call.data == "post_message":
        post_new_message(call.message.chat.id)
    elif call.data == "delete_last_message":
        delete_last_message(call.message.chat.id)
    elif call.data == "pin_last_message":
        pin_last_message(call.message.chat.id)
    elif call.data == "change_channel_name":
        change_channel_name(call.message.chat.id)
    elif call.data == "change_channel_photo":
        change_channel_photo(call.message.chat.id)#yepaki_dev
    elif call.data == "change_channel_description":
        change_channel_description(call.message.chat.id)

#BotRunning ~~
print("Started.")
bot.infinity_polling()