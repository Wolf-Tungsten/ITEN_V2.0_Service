from handler.base import BaseHandler
import routes
from handler.exception import PermissionDeniedError, AuthError, ResourceNotExistError
from tornado.httpclient import AsyncHTTPClient, HTTPRequest, HTTPError
import urllib.parse
import json
from tornado.web import RequestHandler


class HardwareHandler(BaseHandler):
    async def get(self, operation):

        if operation == 'state':
            # Web API
            user_id = await self.user_id
            machine_info = self.model.user_get_machine_info(user_id)
            if machine_info is not None:
                self.write({
                    'has': True,
                    'state': machine_info['state'],
                    'train_name': machine_info['train_name'],
                    'train_amount': machine_info['train_amount'],
                    'train_count': machine_info['train_count']
                })
            else:
                self.write(
                    {
                        'has': False
                    }
                )
        elif operation == 'available':
            # Web API
            available_list = self.model.user_get_available_machine()
            self.write({
                'list': available_list
            })
        elif operation == 'arguments':
            # Machine API
            machine_id = self.get_argument('machine_id')
            arguments = await self.db.machine_arguments.get_arguments(machine_id)
            if arguments is not None:
                self.write({
                    'has': True,
                    'arguments': arguments
                })
            else:
                self.write({
                    'has': False
                })
        else:
            raise ResourceNotExistError('不知道你想干什么')

    async def post(self, operation):
        if operation == 'deploy':
            # Web API
            user_id = await self.user_id
            machine_id = self.get_argument('machine_id')
            train_id = self.get_argument('train_id')
            train_amount = self.get_argument('train_amount')
            state = self.model.user_deploy(user_id, machine_id, train_id, train_amount)
            self.write({
                'flag': state
            })
        elif operation == 'pause':
            # Web API
            self.write({
                'flag': self.model.user_pause(await self.user_id)
            })
        elif operation == 'stop':
            # Web API
            self.write({
                'flag': self.model.user_stop(await self.user_id)
            })
        elif operation == 'resume':
            # Web API
            self.write({
                'flag': self.model.user_resume(await self.user_id)
            })
        elif operation == 'command':
            # Web API
            machine_id = self.get_argument('machine_id')
            command = self.get_argument('command')
            if await self.user_privilege >= 2:
                self.model.user_command(machine_id, command)
                self.write({'flag': True})
            else:
                raise PermissionDeniedError('只允许管理员执行命令')
        elif operation == 'active':
            # Machine API
            machine_id = self.get_argument('machine_id')
            state = self.get_argument('state')
            train_id = self.get_argument('train_id')
            train_name = self.get_argument('train_name')
            train_amount = self.get_argument('train_amount')
            train_count = self.get_argument('train_count')
            state = self.model.hardware_update(machine_id, state, train_id, train_name, train_amount, train_count)
            self.write(state)
        elif operation == 'arguments':
            # Web API
            if await self.user_privilege >=  1:
                machine_id = self.get_argument('machine_id')
                args = self.get_argument('arguments')
                await self.db.machine_arguments.add_arguments(machine_id, args)
                self.write({
                    'flag': True,
                    'arguments': args
                })
            else:
                raise PermissionDeniedError('只允许管理员修改参数')

        else:
            raise ResourceNotExistError('不知道你想干什么')
    async def put(self, operation):
        if operation == 'arguments':
            # Web API
            if await self.user_privilege == 1:
                machine_id = self.get_argument('machine_id')
                args = self.get_argument('arguments')
                await self.db.machine_arguments.update_argu2017ments(machine_id, args)
                self.write({
                    'flag': True,
                    'arguments': args
                })
            else:
                raise PermissionDeniedError('只允许管理员修改参数')




routes.handlers += [
    (r'/hardware/([a-z]+)', HardwareHandler),
]
