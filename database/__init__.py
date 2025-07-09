from motor.motor_asyncio import AsyncIOMotorClient
from configs import *

class Database:

    def __init__(self, url, db_name):
        self.db = AsyncIOMotorClient(url)[db_name]
        self.coll = self.db.users

    async def add_user(self, id):
        """Add a new user if not already present."""
        if not await self.is_present(id):
            await self.coll.insert_one(dict(id=id, api=None, shortner=None))

    async def is_present(self, id):
        """Check if user exists in the database."""
        return bool(await self.coll.find_one({'id': int(id)}))

    async def total_users(self):
        """Return total number of users."""
        return await self.coll.count_documents({})

    async def set_shortner(self, uid, shortner, api):
        """Save shortener URL and API key for a user."""
        await self.coll.update_one(
            {'id': uid},
            {'$set': {'shortner': shortner, 'api': api}},
            upsert=True
        )

    async def get_value(self, key, uid):
        """
        Get the value for a specific key (e.g., 'shortner' or 'api') for the given user.
        Handles missing user gracefully by returning None.
        """
        user = await self.coll.find_one({'id': uid})
        if not user:
            return None
        return user.get(key)


# Create a database instance
db = Database(DATABASE_URL, "TechifyBots")
