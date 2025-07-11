from pyrogram import Client, filters
from pyrogram.types import Message
from configs import API_ID, API_HASH, BOT_TOKEN
from utilities import shorten_urls_in_text
import re

app = Client("ThunderShortnerBot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

# --- Media + caption handler ---
@app.on_message(filters.caption & filters.media)
async def media_caption_handler(client, message: Message):
    original_caption = message.caption
    new_caption = await shorten_urls_in_text(original_caption)

    if new_caption == original_caption:
        return  # No changes, skip reply

    await message.reply_photo(
        photo=message.photo.file_id if message.photo else None,
        video=message.video.file_id if message.video else None,
        document=message.document.file_id if message.document else None,
        caption=new_capti_
