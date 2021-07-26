# -*- coding:utf-8 -*-

# database
# mysql
SQLALCHEMY_DATABASE_URI = 'mysql+cymysql://root:123456@localhost/fua'
#201.135
#SQLALCHEMY_DATABASE_URI = 'mysql+cymysql://root:Mysql-5.7.24@192.168.*.*:*/fua'
SQLALCHEMY_TRACK_MODIFICATIONS = True
SQLALCHEMY_COMMIT_TEARDOWN = True
# 多实例配置
# SQLALCHEMY_BINDS = {
     # 新地址1
#     'dev_fua': 'mysql+cymysql://root:123456@localhost/dev_fua',
     # 新地址2
#     'pro_fua': 'mysql+cymysql://root:123456@localhost/pro_fua',
#}

# mongodb
MONGODB_SETTINGS = {
    'db': 'dev_fua',
    'host': 'localhost',
    #'host': '192.168.*.*',
    'port': 27017,
    'connect': True,
    'username': 'admin',
    'password': '123456',
    'authentication_source': 'admin'
}

# redis
CACHE_REDIS_HOST = 'localhost'
CACHE_REDIS_PORT = '6379'
CACHE_REDIS_PASSWORD = '123456'
CACHE_KEY_PREFIX = ''
CACHE_REDIS_DB = '0'
REDIS_URL = "redis://:123456@localhost:6379/0"

SECRET_KEY = ''

# token有效期一周
TOKEN_EXPIRATION = 7*24*3600

# email
MAIL_SERVER = 'smtp.qq.com'  # 电子邮件服务器地址
MAIL_PORT = 465
MAIL_USE_SSL = True
MAIL_USE_TSL = False
MAIL_USERNAME = '@qq.com'
MAIL_PASSWORD = '*'  # 邮箱申请的授权码
