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
            result.pop('password')
            result.pop('token')
        return result

    async def get_user_info_by_id(self, user_id):
        condition = {'_id': self.ObjectId(user_id)}
        result = await self.collection.find_one(condition)
        if result is not None:
            result['_id'] = str(result['_id'])
            result.pop('password')
            result.pop('token')
        return result

    async def get_user_id_by_token(self, token):
        user_info = await self.get_user_info_by_token(token)
        if user_info is not None:
            return str(user_info['_id'])
        else:
            return None

    # 用于用户名密码登录时的身份验证，会更新token
    async def get_token(self, username, password):
        condition = {'username': username,
                     'password': password}
        result = await self.collection.find_one(condition)
        if result is not None:
            sha256 = hashlib.sha256()
            sha256.update(username.encode('utf8'))
            sha256.update(password.encode('utf8'))
            sha256.update(str(dt.datetime.now().timestamp()).encode('utf8'))
            token = sha256.hexdigest()
            user = {
                'token': token
            }
            await self.update_one_by_id(result['_id'], user)
            return token
        else:
            return None

    async def add_user(self, username, password, phone_number, privilege=0, timer=0):
        sha256 = hashlib.sha256()
        sha256.update(username.encode('utf8'))
        sha256.update(password.encode('utf8'))
        sha256.update(str(dt.datetime.now().timestamp()).encode('utf8'))
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

    async def check_username_available(self, username):
        count = await self.collection.count({'username': username})
        if count > 0:
            return False
        else:
            return True


