"""MD5加密"""
import hashlib
from django.conf import settings


def md5(data):
    # SECRET_KEY是django中配置定义的随机生成一个值
    obj = hashlib.md5(settings.SECRET_KEY.encode('utf-8'))
    obj.update(data.encode('utf-8'))
    return obj.hexdigest()


