from pyrogram.types import Message
from configs import START_TXT, HELP_TXT, ABOUT_TXT
from utilities import set_user_format

async def send_result(bot, message: Message, content: str):
    try:
        await message.reply_text(content, disable_web_page_preview=True)
    except Exception as e:
        print(f"[ERROR] Reply failed: {e}")


async def handle_start(bot, message: Message):
    name = message.from_user.mention if message.from_user else "User"
    await message.reply_text(START_TXT.format(name), disable_web_page_preview=True)


async def handle_help(bot, message: Message):
    await message.reply_text(HELP_TXT, disable_web_page_preview=True)


async def handle_about(bot, message: Message):
    await message.reply_text(ABOUT_TXT.format(bot.me.mention), disable_web_page_preview=True)


async def handle_setformat(bot, message: Message):
    args = message.text.split(maxsplit=1)
    if len(args) != 2:
        await message.reply_text("❌ Usage: /setformat mono | bold | plain")
        return

    fmt = args[1].strip().lower()
    if fmt not in ["mono", "bold", "plain"]:
        await message.reply_text("❌ Invalid format. Use: mono, bold, or plain")
        return

    set_user_format(message.from_user.id, fmt)
    await message.reply_text(f"✅ Font style set to **{fmt}**.")
