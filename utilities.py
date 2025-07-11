import re
import httpx
from configs import SHORTENER_API, SHORTENER_DOMAIN
from logger import LOGGER

url_regex = r"(https?://[^\s]+)"

async def extract_and_shorten_links(text, format_type="mono"):
    try:
        links = re.findall(url_regex, text)
        if not links:
            return text, {}

        shortened_map = {}
        for link in links:
            short_url = await shorten_url(link)
            if short_url:
                if format_type == "bold":
                    short_url_fmt = f"**{short_url}**"
                elif format_type == "mono":
                    short_url_fmt = f"`{short_url}`"
                else:
                    short_url_fmt = short_url
                text = text.replace(link, short_url_fmt)
                shortened_map[link] = short_url_fmt

        return text, shortened_map
    except Exception as e:
        LOGGER.error(f"[extract_and_shorten_links] Error: {e}")
        return text, {}

async def shorten_url(url):
    """ Try Shortzy first, then TinyURL as fallback """
    shortzy_result = await try_shortzy(url)
    if shortzy_result:
        return shortzy_result

    tiny_result = await try_tinyurl(url)
    if tiny_result:
        return tiny_result

    return None  # All failed

async def try_shortzy(url):
    try:
        async with httpx.AsyncClient() as client:
            res = await client.get(
                f"https://{SHORTENER_DOMAIN}/api",
                params={"api": SHORTENER_API, "url": url},
                timeout=10
            )
            data = res.json()
            if data.get("status") == "success":
                return data.get("shortenedUrl") or data.get("short")
    except Exception as e:
        LOGGER.warning(f"[Shortzy] Failed for {url}: {e}")
    return None

async def try_tinyurl(url):
    try:
        async with httpx.AsyncClient() as client:
            res = await client.get(
                f"https://tinyurl.com/api-create.php",
                params={"url": url},
                timeout=10
            )
            if res.status_code == 200:
                return res.text.strip()
    except Exception as e:
        LOGGER.warning(f"[TinyURL] Failed for {url}: {e}")
    return None
