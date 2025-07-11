# 🔗 Telegram ShortLink Bot

A modern Telegram bot to shorten multiple links — in messages or photo captions — using any custom shortener (via [Shortzy](https://github.com/TechifyBots/shortzy)).

---

### ✨ Features

- ✅ Convert any link into a short link via your API
- 🖼️ Supports photo captions
- 💡 Handles multiple links in one message
- 🧠 Uses your own shortener + API
- 📊 Admin-only `/stats` support
- ☁️ Deploy to Heroku, Railway, Render, etc.

---

### ⚙️ ENV Variables

| Name          | Description                  |
|---------------|------------------------------|
| `API_ID`      | Telegram API ID              |
| `API_HASH`    | Telegram API Hash            |
| `BOT_TOKEN`   | From BotFather               |
| `DATABASE_URL`| Mongo URI                    |
| `BASE_URL`    | For ping/web server          |
| `ADMIN_ID`    | Your Telegram User ID        |
| `UPDATES_CHANNEL` | Your updates channel     |
| `SUPPORT_GROUP`   | Support group username   |

---

### 🛠 Setup

```bash
git clone https://github.com/yourusername/shortlink-bot
cd shortlink-bot
pip install -r requirements.txt
python bot.py
