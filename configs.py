from os import getenv as genv

API_ID = genv("API_ID", "")
API_HASH = genv("API_HASH", "")
BOT_TOKEN = genv("BOT_TOKEN", "")
BASE_URL = genv("BASE_URL", "")
DATABASE_URL = genv("DATABASE_URL", "")
SUPPORT_GROUP = genv("SUPPORT_GROUP", "Any_Url_Support")
UPDATES_CHANNEL = genv("UPDATES_CHANNEL", "R2K_Bots")
ADMINS = [int(genv("ADMIN_ID", "123456789"))]  # comma-split if multiple

START_TXT = '''<b>👋 Hello {}, I am your personal ShortLink Bot!

➤ I can convert any links to short links using your own API.
➤ Just send me a message or a photo caption containing links.

💡 Use the help menu to get started!</b>'''

HELP_TXT = '''<b>🛠 HOW TO USE

1. Set your API with: /shortlink yoursite.com your_api_key
2. Send any message with links, and I’ll return the shortened version.
3. It also works with photos + captions!

💰 You can earn by sharing short links from many providers.
Use your referral or monetized domain!

Example:
<code>/shortlink shrinkme.io abc123xyz</code></b>'''

ABOUT_TXT = '''<b>🤖 Bot Info

➤ Name: {}
➤ Developer: @ProfessorR2k
➤ Updates: @R2K_Bots
➤ Support: @Any_Url_Support

✨ Built with Pyrogram, MongoDB, and Shortzy.</b>'''
