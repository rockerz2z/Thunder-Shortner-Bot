from pyrogram import Client, filters
from pyrogram.types import Message

@Client.on_message(filters.command("start"))
async def start_command(client, message: Message):
    await message.reply_text(
        "👋 Welcome to Thunder Shortner Bot!\n\n"
        "📎 Send me any message with a link, or media with captioned links.\n"
        "🔗 I will shorten the URLs and send back the same content with updated links.\n\n"
        "Try sending a photo with a caption like: 'Check this: https://youtube.com'",
        quote=True
    )

@Client.on_message(filters.command("help"))
async def help_command(client, message: Message):
    await message.reply_text(
        "🛠 *Bot Help Guide*\n\n"
        "• Send any text with URLs ➜ Bot replies with shortened version.\n"
        "• Send photos/videos/docs with link captions ➜ Bot resends media with updated caption.\n"
        "• Supports multiple links in one message.\n\n"
        "No need to use commands — just drop your links!",
        parse_mode="markdown",
        quote=True
    )
