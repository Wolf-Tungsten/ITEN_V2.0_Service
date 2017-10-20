from tornado.web import RequestHandler
from handler.exception import PermissionDeniedError, AuthError
from handler.exception import ArgsError,MissingArgumentError,PermissionDeniedError
import json

DEFAULT_TYPE = []


class BaseHandler(RequestHandler):

    @property
    def db(self):
        return self.settings['orm'].db

    @property
    def model(self):
        return self.settings['orm'].model

    @property
    async def user_id(self):
        token = self.get_secure_cookie('token')
        user_id = await self.db.user.get_user_id_by_token(token)
        if user_id is None:
            raise AuthError('登录过期，请重新登录')
        else:
            return user_id

