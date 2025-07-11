from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from database import db
from configs import *
from utilities import short_link, save_data
import re


@Client.on_message(filters.command("start") & filters.private)
async def start_handler(c, m):
    await db.add_user(m.from_user.id)
    keyboard = InlineKeyboardMarkup(
        [
            [InlineKeyboardButton("🔱 Help", callback_data="help"),
             InlineKeyboardButton("💰 Earn", callback_data="earn_money")],
            [InlineKeyboardButton("📢 Channel", url="https://t.me/" + UPDATES_CHANNEL),
             InlineKeyboardButton("🛠 Repo", url="https://t.me/ProfessorR2k")],
            [InlineKeyboardButton("❌ Close", callback_data="delete")]
        ]
    )
    await m.reply_text(
        START_TXT.format(m.from_user.mention),
        reply_markup=keyboard
    )


@Client.on_message(filters.command("shortlink") & filters.private)
async def save_shortlink(c, m):
    if len(m.command) < 3:
        await m.reply_text(
            "❌ <b>Invalid format.</b>\nUse:\n<code>/shortlink domain.com API_KEY</code>"
        )
        return
    url = m.command[1].replace("https://", "").replace("http://", "").strip()
    api = m.command[2].strip()
    success = await save_data(url, api, uid=m.from_user.id)
    if success:
        await m.reply_text("✅ Shortener saved successfully.")
    else:
        await m.reply_text("❌ Failed to validate shortener or API.")


@Client.on_message(filters.command("stats") & filters.user(ADMINS))
async def stats_handler(c, m):
    total = await db.total_users()
    await m.reply_text(f"👥 Total Users: <b>{total}</b>")


@Client.on_message(filters.command("setformat") & filters.private)
async def set_format(c, m):
    if len(m.command) < 2:
        return await m.reply_text("Usage: /setformat bold | italic | mono | plain")
    
    fmt = m.command[1].lower()
    if fmt not in ["bold", "italic", "mono", "plain"]:
        return await m.reply_text("❌ Invalid. Use: bold | italic | mono | plain")
    
    await db.set_format(m.from_user.id, fmt)
    await m.reply_text(f"✅ Format set to <b>{fmt}</b>.")


@Client.on_message(filters.command("setcaption") & filters.private)
async def set_caption(c, m):
    if len(m.text.split(None, 1)) < 2:
        return await m.reply_text("Usage:\n<code>/setcaption Your caption text</code>")
    
    caption = m.text.split(None, 1)[1]
    await db.set_caption(m.from_user.id, caption)
    await m.reply_text("✅ Caption updated.")


@Client.on_message(filters.private & (filters.text | (filters.photo & filters.caption)))
async def auto_shortener(c, m):
    uid = m.from_user.id
    text = m.caption if m.caption else m.text or ""
    links = re.findall(r'https?://\S+', text)
    if not links:
        return

    fmt = await db.get_value("format", uid) or "plain"
    cap = await db.get_value("caption", uid) or ""

    def apply_format(link):
        if fmt == "bold":
            return f"<b>{link}</b>"
        elif fmt == "italic":
            return f"<i>{link}</i>"
        elif fmt == "mono":
            return f"<code>{link}</code>"
        else:
            return link

    short_links = []
    for link in links:
        try:
            short = await short_link(link, uid)
            short_links.append(apply_format(short))
        except:
            pass  # skip on failure

    final = cap + "\n" + "\n".join(short_links)

    if m.photo:
        await m.reply_photo(m.photo.file_id, caption=final)
    else:
        await m.reply_text(final)
