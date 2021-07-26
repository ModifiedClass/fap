# -*- coding:utf-8 -*-

from app.app import Flask
from app.middlewares.hooks import load_middleware


# 蓝图注册到核心对象
def register_blueprints(a):
    from app.api.v1 import create_blueprint_v1
    from app.web_socket import create_blueprint_socket
    a.register_blueprint(create_blueprint_v1(), url_prefix='/api/v1')
    a.register_blueprint(create_blueprint_socket(), url_prefix='/sock')


# 创建mysql数据库
def register_plugin(a):
    from app.models.mysql.base import db
    db.init_app(a)
    with a.app_context():
        with db.auto_commit():
            db.create_all()


# 连接mongodb数据库
def register_mongodb(a):
    from app.models.mongodb.base import db
    db.init_app(a)

# 连接redis数据库
def register_redis_db(a):
    from app.models.redis.base import db
    db.init_app(a)


# 使用缓存
"""
def register_cache(a):
    from app.libs.cache import cache
    cache.init_app(a)
"""


# mail
def register_mail(a):
    from app.libs.email import mail
    mail.init_app(a)


def create_app():
    
    a = Flask(__name__)
    a.config.from_object('app.config.secure')
    a.config.from_object('app.config.setting')
    register_plugin(a)
    register_mongodb(a)
    register_redis_db(a)
    # register_cache(a)
    register_mail(a)
    register_blueprints(a)
    load_middleware(a)
    
    return a
