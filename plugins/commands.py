from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from database import db
from configs import *
from utilities import short_link, save_data
import re


@Client.on_message(filters.command('start') & filters.private)
async def start_handler(c, m):
    try:
        await db.add_user(m.from_user.id)
        keyboard = InlineKeyboardMarkup(
            [
                [InlineKeyboardButton("Hᴇʟᴩ Mᴇɴᴜ 🔱", callback_data="help"),
                 InlineKeyboardButton("Eᴀʀɴ Mᴏɴᴇʏ ❣️", callback_data="earn_money")],
                [InlineKeyboardButton("Cʜᴀɴɴᴇʟ 🍩", url="https://telegram.me/R2K_Bots"),
                 InlineKeyboardButton("Rᴇᴘᴏ 🛠", url="https://telegram.me/ProfessorR2k")],
                [InlineKeyboardButton("Cʟᴏsᴇ ❌", callback_data="delete")]
            ]
        )

        await m.reply_text(
            START_TXT.format(m.from_user.mention),
            reply_markup=keyboard
        )
    except:
        pass


@Client.on_message(filters.command('shortlink') & filters.private)
async def save_shortlink(c, m):
    if len(m.command) < 3:
        await m.reply_text(
            "<b>🕊️ Cᴏᴍᴍᴀɴᴅ Iɴᴄᴏᴍᴘʟᴇᴛᴇ :\n\nPᴜᴛ Sʜᴏʀᴛɴᴇʀ URL & API Aʟᴏɴɢ Wɪᴛʜ Tʜᴇ Cᴏᴍᴍᴀɴᴅ .\n\nEx: <code>/shortlink example.com api</code> \n ⚡ Uᴘᴅᴀᴛᴇs - @R2K_Bots</b>"
        )
        return
    usr = m.from_user
    elg = await save_data(
        (m.command[1].replace("/", "").replace("https:", "").replace("http:", "")),
        m.command[2],
        uid=usr.id
    )
    if elg:
        await m.reply_text("✅ Shortner set successfully.")
    else:
        await m.reply_text("❌ Invalid API or Site URL.")


# ✅ NEW: Auto-shortens multiple links in text or caption (photo)
@Client.on_message((filters.text | filters.photo) & filters.private)
async def multi_link_shortener(client, message):
    uid = message.from_user.id
    text = message.caption or message.text or ""

    # Extract all URLs using regex
    links = re.findall(r'https?://\S+', text)

    if not links:
        return  # No reply if no valid links are found

    result_lines = []
    for link in links:
        try:
            short = await short_link(link, uid)
            result_lines.append(f"`{short}`")
        except Exception:
            result_lines.append(f"❌ Failed: {link}")

    if result_lines:
        await message.reply_text("\n".join(result_lines))
