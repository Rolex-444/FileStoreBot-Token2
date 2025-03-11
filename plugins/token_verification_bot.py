import json
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, MessageHandler, Filters, CallbackContext

# File to store user progress
USER_DATA_FILE = "user_data.json"
TOKEN_FILE = "valid_tokens.json"

# Sample video file paths (Replace with actual Telegram video file IDs or URLs)
VIDEOS = [
    "video_1.mp4",
    "video_2.mp4",
    "video_3.mp4",
    "video_4.mp4",  # Locked without token
]

# Load user data
def load_user_data():
    try:
        with open(USER_DATA_FILE, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return {}

# Save user data
def save_user_data(data):
    with open(USER_DATA_FILE, "w") as file:
        json.dump(data, file)

# Load valid tokens
def load_valid_tokens():
    try:
        with open(TOKEN_FILE, "r") as file:
            return json.load(file)["tokens"]
    except FileNotFoundError:
        return []

# Start command
def start(update: Update, context: CallbackContext) -> None:
    user_id = str(update.message.chat_id)
    user_data = load_user_data()

    if user_id not in user_data:
        user_data[user_id] = {"videos_watched": 0, "verified": False}
        save_user_data(user_data)

    send_video(update, context, user_id)

# Send videos based on user progress
def send_video(update: Update, context: CallbackContext, user_id: str) -> None:
    user_data = load_user_data()
    user_info = user_data.get(user_id, {"videos_watched": 0, "verified": False})
    
    if user_info["videos_watched"] < 3:
        video_index = user_info["videos_watched"]
        context.bot.send_video(chat_id=user_id, video=open(VIDEOS[video_index], "rb"))
        
        user_info["videos_watched"] += 1
        user_data[user_id] = user_info
        save_user_data(user_data)

        if user_info["videos_watched"] < 3:
            keyboard = [[InlineKeyboardButton("Next Video", callback_data="next_video")]]
            reply_markup = InlineKeyboardMarkup(keyboard)
            context.bot.send_message(chat_id=user_id, text="Click below for the next video.", reply_markup=reply_markup)
        else:
            context.bot.send_message(chat_id=user_id, text="You've watched 3 videos! Enter a valid token to continue.")

    elif user_info["verified"]:
        context.bot.send_video(chat_id=user_id, video=open(VIDEOS[3], "rb"))
    else:
        context.bot.send_message(chat_id=user_id, text="Enter a valid token to continue.")

# Handle "Next Video" button
def button(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    user_id = str(query.message.chat_id)
    query.answer()
    send_video(update, context, user_id)

# Handle token input
def token_input(update: Update, context: CallbackContext) -> None:
    user_id = str(update.message.chat_id)
    token = update.message.text.strip()
    valid_tokens = load_valid_tokens()
    user_data = load_user_data()

    if token in valid_tokens:
        user_data[user_id] = {"videos_watched": 3, "verified": True}
        save_user_data(user_data)
        update.message.reply_text("Token verified! You can now watch more videos.")
        send_video(update, context, user_id)
    else:
        update.message.reply_text("Invalid token. Please enter a valid token.")

# Main function to set up the bot
def main():
    TOKEN = "YOUR_TELEGRAM_BOT_TOKEN"
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CallbackQueryHandler(button))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, token_input))

    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
          
