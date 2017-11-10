from handler.base import BaseHandler
import routes
from handler.exception import PermissionDeniedError, AuthError, ResourceNotExistError
from tornado.httpclient import AsyncHTTPClient, HTTPRequest, HTTPError
import urllib.parse
import json
from tornado.web import RequestHandler


class TrainModeHandler(BaseHandler):
    async def get(self, operator):
        if operator == 'available':
            available_list = await self.db.train_mode.get_train_mode_list()
            self.write({
                'available_list': available_list
            })
        elif operator == 'data':
            train_id = self.get_argument('train_id')
            data = await self.db.train_mode.get_train_data(train_id)
            self.write(data)
        else:
            raise ResourceNotExistError('不知道你想干什么')

    async def post(self, operator):
        if await self.user_privilege > 0:
            train_name = self.get_argument('train_name')
            train_data = self.get_argument('train_data')
            await self.db.train_mode.add_train_mode(train_name, train_data)
            self.write({'flag': True})
        else:
            raise PermissionDeniedError('只允许管理员添加训练模式')

    async def put(self, operator):
        if await self.user_privilege > 0:
            train_id = self.get_argument('train_id')
            train_name = self.get_argument('train_name')
            train_data = self.get_argument('train_data')
            await self.db.train_mode.update_train_mode(train_id=train_id, train_name=train_name, train_data=train_data)
            self.write({'flag': True})
        else:
            raise PermissionDeniedError('只允许管理员修改训练模式')

    # TODO: 管理员删除训练模式


routes.handlers += [
    (r'/trainmode/([a-z]+)', TrainModeHandler),
]



