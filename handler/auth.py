from handler.base import BaseHandler
import routes
from handler.exception import PermissionDeniedError, AuthError, ResourceNotExistError
from tornado.httpclient import AsyncHTTPClient, HTTPRequest, HTTPError
import urllib.parse
import json
from tornado.web import RequestHandler
from sdk.geetest import GeetestLib
from config import (GEETEST_KEY, GEETEST_ID)
import hashlib



class AuthHandler(BaseHandler):

    async def get(self, operation):

        if operation == 'info':
            user_id = await self.user_id
            user_info = await self.db.user.get_user_info_by_id(user_id)
            self.write(user_info)
        elif operation == 'geetest':
            self.gt = GeetestLib(GEETEST_ID, GEETEST_KEY)
            username = self.get_argument('user_name').encode('utf8')
            sha128 = hashlib.sha256()
            sha128.update(username)

            status = self.gt.pre_process(sha128.hexdigest())
            if not status:
                status = 2
            # self.session[gt.GT_STATUS_SESSION_KEY] = status
            # self.session["user_id"] = user_id
            response_str = self.gt.get_response_str()
            self.write(response_str)
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
        elif operation == 'websignin':
            self.gt = GeetestLib(GEETEST_ID, GEETEST_KEY)
            username = self.get_argument('username')
            password = self.get_argument('password')
            challenge = self.get_argument('geetest_challenge')
            validate = self.get_argument('geetest_validate')
            seccode = self.get_argument('geetest_seccode')
            result = self.gt.success_validate(challenge, validate, seccode, 'iten')
            if result:
                new_token = await self.db.user.get_token(username, password)
                if new_token is not None:
                    self.set_cookie('token', new_token)
                    self.write({'flag': True, 'token': new_token})
                else:
                    raise AuthError('用户名或密码错误')
            else:
                raise PermissionDeniedError('未通过人机交互认证')
        elif operation == 'sms':
            self.gt = GeetestLib(GEETEST_ID, GEETEST_KEY)
            username = self.get_argument('username')
            available = await self.db.user.check_username_available(username)
            if available:
                phone_number = self.get_argument('phone_number')
                challenge = self.get_argument('geetest_challenge')
                validate = self.get_argument('geetest_validate')
                seccode = self.get_argument('geetest_seccode')
                result = self.gt.success_validate(challenge, validate, seccode, 'iten')
                if result:
                    flag = self.model.user_send_sms(phone_number)
                    if flag:
                        self.write({'flag': flag})
                    else:
                        self.write({'flag': flag, 'msg': '短信发送过于频繁，请稍候重试'})
                else:
                    self.write({'flag': False, 'msg': '没有通过人机验证'})
            else:
                self.write({'flag': False, 'msg': '用户名已注册，请选择其他用户名！'})
        elif operation == 'signup':
            username = self.get_argument('username')
            password = self.get_argument('password')
            phone_number = self.get_argument('phone_number')
            sms_token = self.get_argument('sms_token')
            if self.model.user_check_sms(phone_number, sms_token):
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