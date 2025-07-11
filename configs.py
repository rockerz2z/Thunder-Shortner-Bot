import os

# Telegram API credentials
API_ID = int(os.getenv("API_ID", "123456"))         # Replace with your API ID
API_HASH = os.getenv("API_HASH", "your_api_hash")   # Replace with your API HASH
BOT_TOKEN = os.getenv("BOT_TOKEN", "your_bot_token")  # Replace with your bot token

# Shortzy API Key
SHORTZY_API = os.getenv("SHORTZY_API", "your_shortzy_api_key")  # Replace with your Shortzy API key
