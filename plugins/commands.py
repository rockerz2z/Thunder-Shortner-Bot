from pyrogram.types import Message
from pymongo import MongoClient
from configs import DATABASE_URL

client = MongoClient(DATABASE_URL)
db = client["shortlink_bot"]
users = db["users"]


async def handle_shortlink(bot, message: Message):
    args = message.text.split(maxsplit=2)
    if len(args) != 3:
        await message.reply_text("❌ Usage: /shortlink yourdomain.com your_api_key")
        return

    domain, api = args[1], args[2]
    users.update_one(
        {"_id": message.from_user.id},
        {"$set": {"domain": domain, "api": api}},
        upsert=True
    )
    await message.reply_text(
        f"✅ Shortener settings updated!\n\n"
        f"🔗 Domain: `{domain}`\n🔐 API Key: `{api}`",
        disable_web_page_preview=True
    )


def get_user_shortener(user_id):
    user = users.find_one({"_id": user_id})
    if user and "domain" in user and "api" in user:
        return user["domain"], user["api"]
    return None, None
