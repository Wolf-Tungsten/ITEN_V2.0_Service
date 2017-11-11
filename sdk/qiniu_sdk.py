import config
from qiniu import Auth, BucketManager


def delete_video(key):
    access_key = config.QINIU_ACCESS_KEY
    secret_key = config.QINIU_SECRET_KEY
    # 初始化Auth状态
    q = Auth(access_key, secret_key)
    # 初始化BucketManager
    bucket = BucketManager(q)
    # 你要测试的空间， 并且这个key在你空间中存在
    bucket_name = config.QINIU_BUCKET
    # 删除bucket_name 中的文件 key
    ret, info = bucket.delete(bucket_name, key)
