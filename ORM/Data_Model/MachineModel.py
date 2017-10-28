import queue
import datetime as dt
import utility.log as log

stateList = ['working', 'free', 'pause', 'deploying']


class MachineModel(object):

    def __init__(self, machine_id, state='free', train_id=''
                 ,train_name='', train_amount=0, train_count=0):
        self.machine_id = machine_id
        self.state = state
        self.command = queue.Queue()
        self.train_name = train_name
        self.train_id = train_id
        self.train_amount = train_amount
        self.train_count = train_count
        self.alive = dt.datetime.now().timestamp()

    def user_get_state(self):
        return {
            'machine_id': self.machine_id,
            'state': self.state,
            'train_name': self.train_name,
            'train_amount': self.train_amount,
            'train_count': self.train_count
        }

    def hardware_state(self, state='free', train_id='', train_name='',
                       train_amount=0, train_count=0):

        want_to_return = {
            'state': self.state,
            'train_id': self.train_id,
            'train_amount': self.train_amount
        }
        self.alive = dt.datetime.now().timestamp()
        if self.state == 'deploying':
            # 如果当前模型状态被置为deploying
            if state == 'working':
                # 网球机汇报状态为working，证明任务部署成功，更新模型信息保持同步
                self.state = 'working'
                self.train_amount = train_amount
                self.train_count = train_count
                self.train_id = train_id
                self.train_name = train_name
                want_to_return['state'] = 'working'
                want_to_return['train_id'] = self.train_id
                want_to_return['train_amount'] = self.train_amount
            elif state == 'free':
                # 网球机汇报状态为free，证明任务没有部署成功，应继续部署任务，不改变状态
                want_to_return['state'] = 'deploying'
                want_to_return['train_id'] = self.train_id
                want_to_return['train_amount'] = self.train_amount
            else:
                # 出现其他情况
                log.error_log('出现向非free状态机器部署任务的情况')
        elif self.state == 'free' or self.state == 'pause':
            # 如果当前模型状态被置为pause或者stop
            if state == 'working':
                # 网球机汇报状态为working，机器没有被暂停或停止，继续下达暂停或停止状态
                want_to_return['state'] = self.state
                self.train_count = train_count  # 可能计数还在更新，所以需要跟进
            elif state == 'pause' or state == 'free':
                self.state = state
            else:
                log.error_log('出现向deploying状态的机器下达暂停或停止命令情况')
        elif self.state == 'working':
            # 如果网球机模型为置为working状态，仅更新状态即可
            if state != 'pause':
                self.state = state
            self.train_amount = train_amount
            self.train_id = train_id
            self.train_count = train_count
            self.train_name = train_name
        else:
            pass
        # 读取该机命令队列，如果命令队列为空则保持command为空，否则返回之前插入的command
        want_to_return['command'] = ''
        if self.command.empty():
            pass
        else:
            want_to_return['command'] = self.command.get()
        return want_to_return

    def user_deploy(self, train_id, train_amount):
        # 只有对没有任务进行的机器才能部署任务，此处为防呆检查
        if self.state == 'free':
            self.state = 'deploying'
            self.train_id = train_id
            print(self.train_id)
            self.train_amount = train_amount

    def user_stop(self):
        # 处于deploy状态的机器停止相当于释放
        self.state = 'free'
        return True

    def user_pause(self):
        if self.state == 'working':
            self.state = 'pause'
            return True
        else:
            return False

    def user_resume(self):
        if self.state == 'pause':
            self.state = 'working'
            return True
        else:
            return False

    def user_command(self, command):
        self.command.put(command)






