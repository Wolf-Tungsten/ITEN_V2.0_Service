from handler.base import BaseHandler
import routes
from handler.exception import PermissionDeniedError, AuthError, ResourceNotExistError
from tornado.httpclient import AsyncHTTPClient, HTTPRequest, HTTPError
import urllib.parse
import json
from tornado.web import RequestHandler


class AuthHandler(BaseHandler):
    async def get(self, operation):
        if operation == 'info':
            user_id = await self.user_id
            user_info = await self.db.user.get_user_info_by_id(user_id)
            self.write(user_info)
        else:
            raise ResourceNotExistError('身份信息获取请求')

    async def post(self, operation):
        if operation == 'signin':
            username = self.get_argument('username')
            password = self.get_argument('password')
            new_token = await self.db.user.get_token(username, password)
            if new_token is not None:
                self.set_cookie('token', new_token)
                self.write({'flag': True, 'token': new_token})
            else:
                raise AuthError('用户名或密码错误')
        elif operation == 'sms':
            phone_number = self.get_argument('phone_number')
            flag = self.model.user_send_sms(phone_number)
            self.write({'flag': flag})
        elif operation == 'signup':
            username = self.get_argument('username')
            password = self.get_argument('password')
            phone_number = self.get_argument('phone_number')
            sms_token = self.get_argument('sms_token')
            if self.is_debug or self.model.user_check_sms(phone_number, sms_token):
                print(self.is_debug)
                await self.db.user.add_user(username, password, phone_number)
                self.write({'flag': True, 'msg': '新用户注册成功！'})
            else:
                self.write({'flag': False, 'msg': '短信验证码不正确！'})
        else:
            raise ResourceNotExistError('不知道你想干什么')

    async def put(self, operation):
        pass
        # TODO 修改密码逻辑


routes.handlers += [
    (r'/auth/([a-z]+)', AuthHandler),
]