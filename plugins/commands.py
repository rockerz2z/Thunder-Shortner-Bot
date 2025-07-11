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


@Client.on_message(filters.private & (filters.text | (filters.photo & filters.caption)))
async def auto_shortener(c, m):
    uid = m.from_user.id
    text = m.caption if m.caption else m.text or ""

    links = re.findall(r'https?://\S+', text)
    if not links:
        return

    updated = text
    for link in links:
        try:
            short = await short_link(link, uid)
            updated = updated.replace(link, short)
        except:
            pass  # ignore failure

    if m.photo:
        await m.reply_photo(m.photo.file_id, caption=updated)
    else:
        await m.reply_text(updated)
