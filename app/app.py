from flask import Flask as _Flask
from flask.json import JSONEncoder as _JSONEncoder
from datetime import date,datetime

from app.libs.error_code import ServerError


# 重写default自定义序列化json
class JSONEncoder(_JSONEncoder):
    def default(self, o):
        # 模型中定义keys 与 __getitem__ 方法，转换成字典后序列化
        if hasattr(o, 'keys') and hasattr(o, '__getitem__'):
            return dict(o)
        # 无法序列化的对象在此增加格式化方法
        if isinstance(o, date):
            return o.strftime('%Y-%m-%d')
        if isinstance(o, datetime):
            return o.strftime('%Y-%m-%d %H:%M:%S')
        raise ServerError()


# 自定义JSONEncoder覆盖原来json_encoder
class Flask(_Flask):
    json_encoder = JSONEncoder
