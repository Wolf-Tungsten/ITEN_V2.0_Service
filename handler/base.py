from tornado.web import RequestHandler
from handler.exception import PermissionDeniedError, AuthError
from handler.exception import ArgsError,MissingArgumentError,PermissionDeniedError
import json

DEFAULT_TYPE = []


class BaseHandler(RequestHandler):

    # 支持跨域的服务
    def finish(self, chunk=None):
        self.set_header('Access-Control-Allow-Origin', '*')
        self.set_header('Access-Control-Allow-Methods', 'POST, GET, PUT, DELETE')
        super(BaseHandler, self).finish(chunk)

    def options(self):
        self.finish()

    @property
    def db(self):
        return self.settings['orm'].db

    @property
    def model(self):
        return self.settings['orm'].model

    @property
    def is_debug(self):
        return self.settings['debug']

    @property
    async def user_id(self):
        # token = self.get_secure_cookie('token')
        headers = self.request.headers
        token = None
        if 'Access-Token' in headers:
            token = headers['Access-Token']
        user_id = await self.db.user.get_user_id_by_token(token)
        if user_id is None:
            raise AuthError('登录过期，请重新登录')
        else:
            return user_id

    @property
    async def user_privilege(self):
        user_id = await self.user_id
        user_info = await self.db.user.get_user_info_by_id(user_id)
        return user_info['privilege']

