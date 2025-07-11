from pyrogram import Client, filters
from pyrogram.types import Message
from configs import API_ID, API_HASH, BOT_TOKEN
from utilities import shorten_urls_in_text, upload_to_telegraph

app = Client("ThunderShortnerBot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

# --- Media with caption handler (shorten URLs in captions) ---
@app.on_message(filters.caption & filters.media)
async def media_caption_handler(client, message: Message):
    original_caption = message.caption
    new_caption = await shorten_urls_in_text(original_caption)

    if new_caption == original_caption:
        return

    await message.reply_media_group(
        [message] if not message.media_group_id else [],
        quote=True
    ) if message.media_group_id else await message.reply(
        photo=message.photo.file_id if message.photo else None,
        video=message.video.file_id if message.video else None,
        document=message.document.file_id if message.document else None,
        caption=new_caption,
        parse_mode="html"
    )

# --- Text-only messages ---
@app.on_message(filters.text & ~filters.command(["start", "help"]))
async def text_message_handler(client, message: Message):
    original_text = message.text
    new_text = await shorten_urls_in_text(original_text)

    if new_text != original_text:
        await message.reply_text(new_text, parse_mode="html")

# --- Photo-only messages (upload to Telegraph) ---
@app.on_message(filters.photo & ~filters.caption)
async def photo_only_handler(client, message: Message):
    link = await upload_to_telegraph(client, message)
    if link:
        await message.reply_text(f"🖼 Uploaded to Telegraph:\n{link}")
    else:
        await message.reply_text("❌ Failed to upload to Telegraph.")

# --- Start command ---
@app.on_message(filters.command("start"))
async def start(client, message):
    await message.reply_text(
        "👋 Hello! Send me a link, photo with caption, or video with URLs.\n"
        "I'll shorten links and resend your content — or upload photo-only messages to Telegraph."
    )

if __name__ == "__main__":
    app.run()
