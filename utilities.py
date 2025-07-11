from configs import *
from aiohttp import web
from shortzy import Shortzy
import asyncio, logging, aiohttp, traceback
from database import db

routes = web.RouteTableDef()

@routes.get("/", allow_head=True)
async def root_handler(request):
    return web.json_response("🚀 ShortLink Bot is alive!")

async def web_server():
    app = web.Application(client_max_size=30000000)
    app.add_routes(routes)
    return app

async def ping_server():
    while True:
        await asyncio.sleep(600)
        try:
            async with aiohttp.ClientSession(
                timeout=aiohttp.ClientTimeout(total=10)
            ) as session:
                async with session.get(BASE_URL) as resp:
                    logging.info(f"✅ Ping success: {resp.status}")
        except Exception:
            logging.warning("⚠️ Failed to ping BASE_URL")

async def short_link(link, uid):
    usite = await db.get_value("shortner", uid)
    uapi = await db.get_value("api", uid)
    if not usite or not uapi:
        raise ValueError("Missing API setup")
    shortzy = Shortzy(api_key=uapi, base_site=usite)
    return await shortzy.convert_from_text(link)

async def save_data(tst_url, tst_api, uid):
    try:
        shortzy = Shortzy(api_key=tst_api, base_site=tst_url)
        test = await shortzy.convert("https://telegram.me/" + UPDATES_CHANNEL)
        if test.startswith("http"):
            await db.set_shortner(uid, shortner=tst_url, api=tst_api)
            return True
    except Exception:
        pass
    return False
