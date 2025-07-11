from pyrogram import Client, filters
from pyrogram.types import Message
from utilities import extract_and_shorten_links
from configs import API_ID, API_HASH, BOT_TOKEN, SHORTENER_API, SHORTENER_DOMAIN
import re

bot = Client("ShortLinkBot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)


@bot.on_message(filters.private & filters.incoming & ~filters.command(["start", "help", "about"]))
async def shorten_links(client: Client, message: Message):
    original_msg = message.text or message.caption
    if not original_msg:
        return

    # Extract all links
    urls = re.findall(r'https?://[^\s]+', original_msg)
    if not urls:
        return

    # Shorten all URLs
    try:
        short_map = await extract_and_shorten_links(urls, SHORTENER_API, SHORTENER_DOMAIN)
    except Exception as e:
        await message.reply_text(f"❌ Error shortening links:\n<code>{e}</code>")
        return

    # Replace only links in the text
    new_text = original_msg
    for old_link, new_link in short_map.items():
        new_text = new_text.replace(old_link, new_link)

    # Detect message type and send back same type
    if message.photo:
        await message.reply_photo(
            photo=message.photo.file_id,
            caption=new_text,
            parse_mode="HTML"
        )
    elif message.video:
        await message.reply_video(
            video=message.video.file_id,
            caption=new_text,
            parse_mode="HTML"
        )
    elif message.document:
        await message.reply_document(
            document=message.document.file_id,
            caption=new_text,
            parse_mode="HTML"
        )
    elif message.audio:
        await message.reply_audio(
            audio=message.audio.file_id,
            caption=new_text,
            parse_mode="HTML"
        )
    elif message.voice:
        await message.reply_voice(
            voice=message.voice.file_id,
            caption=new_text,
            parse_mode="HTML"
        )
    elif message.animation:
        await message.reply_animation(
            animation=message.animation.file_id,
            caption=new_text,
            parse_mode="HTML"
        )
    else:
        await message.reply_text(new_text, parse_mode="HTML")


print(">> Bot started. Press Ctrl+C to stop.")
bot.run()
