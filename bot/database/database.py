import motor.motor_asyncio

class Database:

    def __init__(self, uri, database_name):
        self._client = motor.motor_asyncio.AsyncIOMotorClient(uri)
        self.db = self._client[database_name]
        self.col = self.db.users
        self.channel = self.db.channel

    async def new_channel(self, channel_id):
        channel = {
            'channel_id': channel_id,
            'text': "Hello {name}, Your Request to Join {chat} has been Approved!\n\nSend /start to know more.",
            'buttons': None
        }
        await self.channel.insert_one(channel)

    async def get_welcome(self, channel_id):
        channel = await self.channel.find_one({'channel_id': channel_id})
        if not channel:
            await self.new_channel(channel_id)
            return await self.get_welcome_text(channel_id)
        return channel.get('text', None), channel.get('buttons', None)

    async def update_welcome(self, channel_id, text, buttons):
        channel = await self.channel.find_one({'channel_id': channel_id})
        if not channel:
            await self.new_channel(channel_id)
            return await self.update_welcome(channel_id, text, buttons)
        await self.channel.update_one({'channel_id': channel_id}, {'$set': {'text': text, 'buttons': buttons}})
        
    async def add_user(self, id):
        user = dict(id=id)
        await self.col.insert_one(user)

    async def is_user_exist(self, id):
        user = await self.col.find_one({'id': int(id)})
        return True if user else False

    async def total_users_count(self):
        count = await self.col.count_documents({})
        return count

    async def get_all_users(self):
        all_users = self.col.find({}).batch_size(10)
        return all_users

    async def delete_user(self, user_id):
        await self.col.delete_many({'id': int(user_id)})
