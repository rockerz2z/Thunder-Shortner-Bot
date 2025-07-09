from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from database import db
from configs import *
from utilities import short_link, save_data


@Client.on_message(filters.command('start') & filters.private)
async def start_handler(c, m):
    try:
        await db.add_user(m.from_user.id)
        keyboard = InlineKeyboardMarkup(
            [
                [InlineKeyboardButton("Hᴇʟᴩ Mᴇɴᴜ 🔱", callback_data="help")],
                [InlineKeyboardButton("Cʜᴀɴɴᴇʟ 🍩", url="https://telegram.me/R2K_Bots"),
                 InlineKeyboardButton("Rᴇᴘᴏ 🛠", url="https://telegram.me/ProfessorR2k")],
                [InlineKeyboardButton("Cʟᴏsᴇ ❌", callback_data="delete")]
            ]
        )
        await m.reply_text(
            START_TXT.format(m.from_user.mention),
            reply_markup=keyboard
        )
    except Exception as e:
        print(f"Start handler error: {e}")


@Client.on_message(filters.command('shortlink') & filters.private)
async def save_shortlink(c, m):
    if len(m.command) < 3:
        await m.reply_text(
            "<b>🕊️ Cᴏᴍᴍᴀɴᴅ Iɴᴄᴏᴍᴘʟᴇᴛᴇ:\n\n"
            "Pᴜᴛ Sʜᴏʀᴛɴᴇʀ URL & API Aʟᴏɴɢ Wɪᴛʜ Tʜᴇ Cᴏᴍᴍᴀɴᴅ.\n\n"
            "Ex: <code>/shortlink example.com api_key</code>\n"
            "⚡ Uᴘᴅᴀᴛᴇs - @R2K_Bots</b>"
        )
        return

    usr = m.from_user
    shortner_url = m.command[1].replace("/", "").replace("https:", "").replace("http:", "")
    api_key = m.command[2]

    saved = await save_data(shortner_url, api_key, uid=usr.id)
    if saved:
        await m.reply_text(
            f"📍 Sʜᴏʀᴛɴᴇʀ Hᴀs Bᴇᴇɴ Sᴇᴛ Sᴜᴄᴄᴇssғᴜʟʟʏ!\n\n"
            f"Sʜᴏʀᴛɴᴇʀ URL - `{await db.get_value('shortner', uid=usr.id)}`\n"
            f"Shortner API - `{await db.get_value('api', uid=usr.id)}`\n"
            f"⚡ Uᴘᴅᴀᴛᴇs - @R2K_Bots"
        )
    else:
        await m.reply_text(
            "🌶️ Eʀʀᴏʀ:\n\n"
            "Yᴏᴜʀ Sʜᴏʀᴛɴᴇʀ API or URL Is Iɴᴠᴀʟɪᴅ.\n"
            "Pʟᴇᴀsᴇ Cʜᴇᴄᴋ Aɢᴀɪɴ!"
        )


@Client.on_message(filters.text & filters.private)
async def shorten_link(_, m):
    txt = m.text
    if not ("http://" in txt or "https://" in txt):
        await m.reply_text("⚠️ Send a valid URL that starts with http:// or https:// to shorten.")
        return

    usr = m.from_user
    shortner_url = await db.get_value("shortner", uid=usr.id)
    api_key = await db.get_value("api", uid=usr.id)

    if not shortner_url or not api_key:
        await m.reply_text(
            "❗ You haven't set your shortener yet.\n\n"
            "Use the command:\n<code>/shortlink example.com your_api_key</code>"
        )
        return

    try:
        short = await short_link(link=txt, uid=usr.id)
        msg = f"__Hᴇʀᴇ ᴀʀᴇ ʏᴏᴜʀ Sʜᴏʀᴛ Lɪɴᴋs__:\n\n<code>{short}</code>"
        await m.reply_text(msg)
    except Exception as e:
        await m.reply_text(f"Error shortening link: {e}")
