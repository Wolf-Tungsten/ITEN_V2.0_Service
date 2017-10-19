from ..collections.base import CollectionBase
import hashlib
import datetime as dt
class UserCollection(CollectionBase):
    def __init__(self, db):
        CollectionBase.__init__(self, db, 'user')

    async def get_user_info_by_token(self, token):
        condition = {'token': token}
        result = await self.collection.find_one(condition)
        if result is not None:
            result['_id'] = str(result['_id'])
        return result

    async def get_user_info_by_id(self, user_id):
        condition = {'_id': self.ObjectId(user_id)}
        result = await self.collection.find_one(condition)
        if result is not None:
            result['_id'] = str(result['_id'])
        return result

    async def get_user_id_by_token(self, token):
        user_info = await self.get_user_info_by_token(token)
        if user_info is not None:
            return user_info['token']
        else:
            return None

    async def get_token(self, username, password):
        condition = {'username': username,
                     'password': password}
        result = await self.collection.find_one(condition)
        if result is not None:
            return result['token']
        else:
            return None

    async def add_user(self, username, password, phone_number, privilege=0, timer=0):
        sha256 = hashlib.sha256()
        sha256.update(username)
        sha256.update(password)
        sha256.update(dt.datetime.now().timestamp())
        token = sha256.hexdigest()
        doc = {
               'username': username,
               'password': password,
               'token': token,
               'privilege': privilege,
               'phone_number': phone_number,
               'timer': timer
               }
        await self.insert_one(doc)

    async def change_password(self, user_id, password):
        current = await self.find_one_by_id(user_id)
        current['password'] = password
        await self.update_one_by_id(user_id, current)

    async def change_phone_number(self, user_id, phone_number):
        current = await self.find_one_by_id(user_id)
        current['phone_number'] = phone_number
        await self.update_one_by_id(user_id, current)

    async def add_train_time(self, user_id, delta):
        current = await self.find_one_by_id(user_id)
        current['timer'] = current['timer'] + delta
        await self.update_one_by_id(user_id, current)


