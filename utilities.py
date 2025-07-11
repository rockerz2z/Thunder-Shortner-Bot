import re
import httpx
from configs import SHORTZY_API

# Regex to detect URLs
URL_REGEX = r'(https?://[^\s]+)'

async def shorten_url(original_url):
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(f"https://shortzy.in/api?api={SHORTZY_API}&url={original_url}")
            data = response.json()
            if data["status"] == "success":
                return data["shortenedUrl"]
            else:
                return original_url  # Fallback to original
    except Exception as e:
        print(f"[ERROR] Failed to shorten: {original_url} — {e}")
        return original_url

async def shorten_urls_in_text(text):
    urls = re.findall(URL_REGEX, text)
    if not urls:
        return text

    updated_text = text
    for url in urls:
        short_url = await shorten_url(url)
        updated_text = updated_text.replace(url, short_url)

    return updated_text
