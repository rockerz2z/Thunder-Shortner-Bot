from pyrogram import Client, filters
from pyrogram.types import Message
from configs import API_ID, API_HASH, BOT_TOKEN, CHANNEL_ID
from utilities import (
    extract_and_shorten_links,
    apply_format,
    get_user_format,
    handle_image_upload,
    handle_video_preview
)
from callback import send_result
from commands import handle_start, handle_help, handle_about, handle_shortlink, handle_setformat

bot = Client("ShortLinkBot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)


@bot.on_message(filters.command("start") & filters.private)
async def start_command(_, message: Message):
    await handle_start(bot, message)


@bot.on_message(filters.command("help") & filters.private)
async def help_command(_, message: Message):
    await handle_help(bot, message)


@bot.on_message(filters.command("about") & filters.private)
async def about_command(_, message: Message):
    await handle_about(bot, message)


@bot.on_message(filters.command("shortlink") & filters.private)
async def shortlink_command(_, message: Message):
    await handle_shortlink(bot, message)


@bot.on_message(filters.command("setformat") & filters.private)
async def set_format_command(_, message: Message):
    await handle_setformat(bot, message)


@bot.on_message(filters.private & ~filters.command(["start", "help", "about", "shortlink", "setformat"]))
async def catch_all(_, message: Message):
    user_id = message.from_user.id
    font_format = get_user_format(user_id)

    caption = message.caption if message.caption else message.text

    # Extract and shorten all links
    if caption:
        shortened_caption = await extract_and_shorten_links(caption)
        formatted = apply_format(shortened_caption, font_format)
    else:
        formatted = None

    # Handle media types
    media_path = None
    if message.photo:
        # Upload photo to Telegraph
        telegraph_link = await handle_image_upload(message)
        await message.reply_text(f"🖼 Telegraph Link:\n{telegraph_link}")
        return

    elif message.video and message.video.file_name.endswith((".mp4", ".mkv")):
        media_path = await handle_video_preview(message)
        await message.reply_video(media_path, caption=formatted or None)
        return

    elif message.document:
        media_path = await message.download()
        await message.reply_document(media_path, caption=formatted or None)
        return

    elif caption:
        await message.reply_text(formatted)

    # Auto post result to channel
    try:
        if CHANNEL_ID and caption:
            await bot.send_message(CHANNEL_ID, f"📢 New from {message.from_user.mention}:\n{formatted}")
    except Exception as e:
        print(f"Auto-post to channel failed: {e}")


if __name__ == "__main__":
    print("✅ Bot is running...")
    bot.run()
