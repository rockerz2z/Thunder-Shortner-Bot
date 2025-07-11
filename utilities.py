import re
import httpx
import logging
from pyrogram.types import Message
from telegraph import Telegraph
from datetime import datetime
from pytube import YouTube
from moviepy.editor import VideoFileClip
from pymongo import MongoClient
from configs import (
    SHORTENER_API,
    SHORTENER_DOMAIN,
    TELEGRAPH_ACCESS_TOKEN,
    DATABASE_URL
)

logger = logging.getLogger(__name__)

# Setup Telegraph
telegraph = Telegraph()
if TELEGRAPH_ACCESS_TOKEN:
    telegraph.access_token = TELEGRAPH_ACCESS_TOKEN
else:
    telegraph.create_account(short_name="ShortLinkBot")

# Setup MongoDB
client = MongoClient(DATABASE_URL)
db = client["shortlink_bot"]
users = db["users"]

# Regex for all links
LINK_REGEX = r'https?://[^\s]+'


def get_user_format(user_id):
    user = users.find_one({"_id": user_id})
    return user.get("format", "mono") if user else "mono"


def set_user_format(user_id, font_format):
    users.update_one({"_id": user_id}, {"$set": {"format": font_format}}, upsert=True)


def apply_format(text, font_format):
    if font_format == "mono":
        return "\n".join([f"`{line}`" for line in text.splitlines()])
    elif font_format == "bold":
        return "\n".join([f"*{line}*" for line in text.splitlines()])
    return text


async def shorten_link(link: str):
    # Try Shortzy
    try:
        res = httpx.get(
            f"https://{SHORTENER_DOMAIN}/api",
            params={"api": SHORTENER_API, "url": link},
            timeout=10
        )
        data = res.json()
        if data.get("shortenedUrl"):
            return data["shortenedUrl"]
    except Exception as e:
        logger.warning(f"Shortzy failed for {link}: {e}")

    # Fallback to TinyURL
    try:
        res = httpx.get("https://tinyurl.com/api-create.php", params={"url": link}, timeout=10)
        return res.text.strip()
    except Exception as e:
        logger.error(f"Fallback shortening failed: {e}")
        return link


async def extract_and_shorten_links(text: str) -> str:
    links = re.findall(LINK_REGEX, text)
    if not links:
        return text

    for link in links:
        short = await shorten_link(link)
        text = text.replace(link, short)
    return text


async def handle_image_upload(message: Message) -> str:
    path = await message.download()
    try:
        response = telegraph.upload_file(path)
        return f"https://telegra.ph{response[0]['src']}"
    except Exception as e:
        logger.error(f"Telegraph upload failed: {e}")
        return ""


async def handle_video_preview(message: Message) -> str:
    path = await message.download()
    try:
        clip = VideoFileClip(path)
        if clip.duration > 30:
            clip = clip.subclip(0, 30)
        preview_path = path.replace(".mp4", "_preview.mp4").replace(".mkv", "_preview.mp4")
        clip.write_videofile(preview_path, codec="libx264", audio_codec="aac")
        return preview_path
    except Exception as e:
        logger.error(f"Video preview failed: {e}")
        return path
