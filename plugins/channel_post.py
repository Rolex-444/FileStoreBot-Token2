# (C)Codexbotz

import asyncio
from pyrogram import filters, Client
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.errors import FloodWait

from bot import Bot
from config import ADMINS, CHANNEL_ID, DISABLE_CHANNEL_BUTTON
from helper_func import encode

# === Import download counter helpers ===
from database.database import get_user_download_count, increment_user_download_count, db_verify_status

@Bot.on_message(filters.private & filters.user(ADMINS) & ~filters.command(['start','users','broadcast','batch','genlink','stats']))
async def channel_post(client: Client, message: Message):
    user_id = message.from_user.id

    # --- Begin download limit logic ---
    count = await get_user_download_count(user_id)
    verify_status = await db_verify_status(user_id)
    is_verified = verify_status.get('is_verified', False)

    if count >= 3 and not is_verified:
        await message.reply_text(
            "⚠️ You have reached your free download limit of 3 files.\n\nPlease verify your token to continue downloading."
        )
        return  # Block sending more files

    # If under limit or verified, increment counter
    await increment_user_download_count(user_id)
    # --- End download limit logic ---

    reply_text = await message.reply_text("Please Wait...!", quote = True)
    try:
        post_message = await message.copy(chat_id = client.db_channel.id, disable_notification=True)
    except FloodWait as e:
        await asyncio.sleep(e.x)
        post_message = await message.copy(chat_id = client.db_channel.id, disable_notification=True)
    except Exception as e:
        print(e)
        await reply_text.edit_text("Something went Wrong..!!")
        return

    converted_id = post_message.id * abs(client.db_channel.id)
    string = f"get-{converted_id}"
    base64_string = await encode(string)
    link = f"https://t.me/{client.username}?start={base64_string}"

    reply_markup = InlineKeyboardMarkup(
        [[InlineKeyboardButton("📥 Share URL", url=f'https://telegram.me/share/url?url={link}')]]
    )

    await reply_text.edit_text(f"<b>Here is your link</b>:\n\n{link}", reply_markup=reply_markup, disable_web_page_preview = True)
    if not DISABLE_CHANNEL_BUTTON:
        await post_message.edit_reply_markup(reply_markup)

@Bot.on_message(filters.channel & filters.incoming & filters.chat(CHANNEL_ID))
async def new_post(client: Client, message: Message):

    if DISABLE_CHANNEL_BUTTON:
        return

    converted_id = message.id * abs(client.db_channel.id)
    string = f"get-{converted_id}"
    base64_string = await encode(string)
    link = f"https://t.me/{client.username}?start={base64_string}"

    reply_markup = InlineKeyboardMarkup(
        [[InlineKeyboardButton("📥 Share URL", url=f'https://telegram.me/share/url?url={link}')]]
    )
    try:
        await message.edit_reply_markup(reply_markup)
    except Exception as e:
        print(e)
        pass
        
