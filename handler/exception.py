from tornado.web import HTTPError
from handler import error

class MissingArgumentError(HTTPError):
    def __init__(self, arg_name):
        super(MissingArgumentError, self).__init__(
            400, 'Missing argument %s' % arg_name)
        self.arg_name = arg_name
        self.code = error.MISSING_ARGS


class ResourceNotExistError(HTTPError):
    def __init__(self, res_name):
        super(ResourceNotExistError, self).__init__(404, "不存在的:{0}".format(res_name))
        self.arg_name = res_name
        self.code = error.RES_NOT_EXIST


class PermissionDeniedError(HTTPError):
    def __init__(self, res_name):
        super(PermissionDeniedError, self).__init__(403, '用户权限不允许:{0}'.format(res_name))
        self.arg_name = res_name
        self.code = error.PERMISSIONS_DENIED


class StateError(HTTPError):
    def __init__(self, res_name):
        super(StateError, self).__init__(400, "资源状态不可用{0}".format(res_name))
        self.arg_name = res_name
        self.code = error.STATE_ERROR


class ArgsError(HTTPError):
    def __init__(self, res_name):
        super(ArgsError, self).__init__(400, "参数错误:{0}".format(res_name))
        self.arg_name = res_name
        self.code = error.ARGS_ERROR


class RelateResError(HTTPError):
    def __init__(self, res_name):
        super(RelateResError, self).__init__(410, "相关资源不存在或错误:{0}".format(res_name))
        self.arg_name = res_name
        self.code = error.RELATE_RES_ERROR


class FrequencyError(HTTPError):
    def __init__(self, res_name):
        super(FrequencyError, self).__init__(400, "访问过频:{0}".format(res_name))
        self.arg_name = res_name
        self.code = error.FREQUENCY_ERROR


class AuthError(HTTPError):
    def __init__(self,res_name):
        super(AuthError, self).__init__(401, "验证失败:{0}".format(res_name))
        self.arg_name = res_name
        self.code = error.AUTH_ERROR

