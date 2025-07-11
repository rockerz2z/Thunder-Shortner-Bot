from os import getenv as genv

API_ID = genv("API_ID", "")
API_HASH = genv("API_HASH", "")
BOT_TOKEN = genv("BOT_TOKEN", "")
DATABASE_URL = genv("DATABASE_URL", "")
CHANNEL_ID = int(genv("CHANNEL_ID", "0"))  # Optional for auto-posting

SUPPORT_GROUP = genv("SUPPORT_GROUP", "Any_Url_Support")
UPDATES_CHANNEL = genv("UPDATES_CHANNEL", "R2K_Bots")
ADMINS = [int(i) for i in genv("ADMIN_ID", "123456789").split(",")]

START_TXT = '''<b>👋 Hello {}, I am your personal ShortLink Bot!

➤ I can shorten any links using your custom domain.
➤ I preserve original messages, captions, or media.
➤ Supports mp4, mkv, and even photo to Telegraph!

💡 Try sending a message or photo with a link.</b>'''

HELP_TXT = '''<b>🛠 HOW TO USE

1. Set your shortener domain with: 
<code>/shortlink yourdomain.com your_api_key</code>

2. Set your preferred font format:
<code>/setformat mono</code> or <code>/setformat bold</code>

3. Send any message, caption, or file — and I’ll shorten links only!

💡 Media Support:
• Images → Telegraph link
• Videos (.mp4/.mkv) → 30s preview
• Custom formats → mono / bold / plain

🔁 Auto-post to channel (if configured)</b>'''

ABOUT_TXT = '''<b>🤖 Bot Info

➤ Name: {}
➤ Developer: @ProfessorR2k
➤ Updates: @R2K_Bots
➤ Support: @Any_Url_Support

✨ Powered by Pyrogram, MongoDB, and Shortzy APIs</b>'''
