import config
import datetime as dt
import random
from .MachineModel import MachineModel
import sdk.yunpian_sdk as YP


class DataModel(object):
    def __init__(self):
        self.machine_map = {}  # 网球机模型字典
        self.user_machine_map = {}  # 用户-网球机字典
        self.sms_auth = {}  # 手机号码-验证码字典

    def user_get_available_machine(self):
        available_list = []
        for k in self.machine_map:
            if self.machine_map[k].state == 'free' and \
                                    dt.datetime.now().timestamp() - int(self.machine_map[k].alive) < config.MACHINE_LIFE:
                available_list.append(k)
        return available_list

    def get_machine_id(self, user_id):
        if user_id in self.user_machine_map:
            machine_id = self.user_machine_map[user_id]
            machine_state = self.machine_map[machine_id]
            # 如果机器状态为free-训练已经完成-释放网球机
            if machine_state.state == 'free':
                self.user_machine_map.pop(user_id)
                machine_id = None
            return machine_id
        else:
            return None

    def user_get_machine_info(self, user_id):
        machine_id = self.get_machine_id(user_id)
        if machine_id is not None:
            return self.machine_map[machine_id].user_get_state()

    def user_deploy(self, user_id, machine_id, train_id, train_amount):
        if self.machine_map[machine_id].state == 'free':
            # 确认网球机处于空闲状态
            self.user_machine_map[user_id] = machine_id
            # 将用户和网球机绑定写入字典
            self.machine_map[machine_id].user_deploy(train_id, train_amount)
            # 部署任务
            return True
        else:
            return False

    def user_pause(self, user_id):
        machine_id = self.get_machine_id(user_id)
        if machine_id is not None:
            return self.machine_map[machine_id].user_pause()
        else:
            return False

    def user_stop(self, user_id):
        machine_id = self.get_machine_id(user_id)
        if machine_id is not None:
            return self.machine_map[machine_id].user_stop()
        else:
            return False

    def user_resume(self, user_id):
        machine_id = self.get_machine_id(user_id)
        if machine_id is not None:
            return self.machine_map[machine_id].user_resume()
        else:
            return False

    def user_command(self, machine_id, command):
        self.machine_map[machine_id].user_command(command)

    def user_send_sms(self, phone_number):
        if phone_number in self.sms_auth:
            last_timestamp = self.sms_auth[phone_number]['timestamp']
            current_timestamp = dt.datetime.now().timestamp()
            if current_timestamp - last_timestamp < config.SMS_PERIOD:
                return False
                # 验证码已经发送并且低于频率，防止恶意攻击
        sms_token = random.randint(100000, 999999)
        print(sms_token, phone_number)
        sms_token = str(sms_token)
        self.sms_auth[phone_number] = {
            'timestamp': dt.datetime.now().timestamp(),
            'sms_token': sms_token
        }
        # TODO 发送短信逻辑
        r = YP.send_sms(phone_number, sms_token)
        print(r)
        return True

    def user_check_sms(self, phone_number, sms_token):
        if phone_number in self.sms_auth:
            sms_token = str(sms_token)
            last_timestamp = self.sms_auth[phone_number]['timestamp']
            current_timestamp = dt.datetime.now().timestamp()
            if current_timestamp - last_timestamp < config.SMS_LIFE:
                # 检查验证码是否过期
                print('校验结果',sms_token,self.sms_auth[phone_number]['sms_token'])
                auth = (sms_token == self.sms_auth[phone_number]['sms_token'])
                self.sms_auth.pop(phone_number)
                return auth  # 返回校验结果
            else:
                # 验证码过期
                self.sms_auth.pop(phone_number)
                return False
        else:
            return False

    def hardware_update(self, machine_id, state, train_id, train_name, train_amount, train_count):
        if machine_id not in self.machine_map:
            self.machine_map[machine_id] = MachineModel(machine_id,
                                                        train_name=train_name,
                                                        state=state,
                                                        train_id=train_id,
                                                        train_amount=train_amount,
                                                        train_count=train_count
                                                        )
            machine_state = self.machine_map[machine_id].hardware_state(train_name=train_name,
                                                                        state=state,
                                                                        train_id=train_id,
                                                                        train_amount=train_amount,
                                                                        train_count=train_count)
            machine_state['user_id'] = ''
            return machine_state
        else:
            current_user_id = ''
            for k in self.user_machine_map:
                if self.user_machine_map[k] == machine_id:
                    current_user_id = k
            machine_state = self.machine_map[machine_id].hardware_state(state=state,
                                                                        train_id=train_id,
                                                                        train_name=train_name,
                                                                        train_amount=train_amount,
                                                                        train_count=train_count)
            machine_state['user_id'] = current_user_id
            return machine_state


