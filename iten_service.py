import tornado.web
from motor.motor_tornado import MotorClient
from tornado.options import options, define
from ORM.ORM import ORM
import config
import routes
import hashlib
import datetime as dt


define("port", default=5500, help="本地监听端口", type=int)
define("DEBUG", default=True, help="是否开启debug模式", type=bool)
define("TEST", default=True, help="测试服务器，支持跨域访问,推送测试模式", type=bool)
define("db_name", default="iten", help="mongodb数据库名称", type=str)
tornado.options.parse_command_line()

mongodb_client = MotorClient('127.0.0.1:27017')
mongodb_database = mongodb_client[options.db_name]

orm = ORM(mongodb_database)


application = tornado.web.Application(
    handlers=routes.handlers,
    db=mongodb_database,
    orm=orm,
    TEST=options.TEST,
    debug=options.DEBUG,
    compiled_template_cache=True,
    static_hash_cache=True,
    autoreload=True,
    debug_mode=True,
)


if __name__ == "__main__":
    application.listen(options.port)
    ioloop = tornado.ioloop.IOLoop.current()
    ioloop.start()