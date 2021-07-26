# -*- coding:utf-8 -*-

# mongodb记录日志
# pipenv install log4mongo

import logging
import logging.config

"""
config = {
    'version': 1, # 固定写法
    'formatters': { # 格式化
        'simple': { # simple是这个方案的名称
            'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        },
    },
    'handlers': {  # 日志分发函数，根据日志级别进行分发
        'console': { # 控制台输出
            'class': 'logging.StreamHandler', # 日志输出使用的方法
            'level': 'DEBUG', # 输出级别，高于此级别的不输出
            'formatter': 'simple'
        },
        'file': {  # 文件输出
            'class': 'logging.FileHandler',
            'filename': 'logging.log', # 日志文件名
            'level': 'DEBUG',
            'maxBytes': 10485760, # 日志文件大小限制
            'backupCount': 50,  # 日志文件个数限制
            'formatter': 'simple'
        },
        'mongo': { # 数据库输出
            'class': 'log4mongo.handlers.MongoHandler',
            'host': 'localhost',
            'port': 27017,
            'database_name': 'dev_fua', # 日志数据库名称
            'collection': 'requestlogs', # 写入的集合（表名）
            'level': 'DEBUG',
        },
    },
    'loggers': {  # logger是Logging模块的主体，为程序提供记录日志的接口、 判断日志所处级别，并判断是否要过滤、根据其日志级别将该条日志分发给不同handler
        'root': { # logger方案名称
            'handlers': ['console'], #此方案分发的handler
            'level': 'DEBUG',
            # 'propagate': True,
        },
        'simple': {
            'handlers': ['console', 'file'],
            'level': 'WARN',
        },
        'mongo': {
            'handlers': ['console', 'mongo'],
            'level': 'DEBUG',
        }
    }
}
logging.config.dictConfig(config)
logger2 = logging.getLogger('mongo')
logger2.debug('debug message')
logger2.info('info message')
logger2.warning('warn message')
logger2.error('error message')
logger2.critical('critical message')

format常用格式说明
%(levelno)s: 打印日志级别的数值
%(levelname)s: 打印日志级别名称
%(pathname)s: 打印当前执行程序的路径，其实就是sys.argv[0]
%(filename)s: 打印当前执行程序名
%(funcName)s: 打印日志的当前函数
%(lineno)d: 打印日志的当前行号
%(asctime)s: 打印日志的时间
%(thread)d: 打印线程ID
%(threadName)s: 打印线程名称
%(process)d: 打印进程ID
%(message)s: 打印日志信息

级别排序:CRITICAL > ERROR > WARNING > INFO > DEBUG
默认生成的root logger的level是logging.WARNING,低于该级别的就不输出了
debug : 打印全部的日志,详细的信息,通常只出现在诊断问题上
info : 打印info,warning,error,critical级别的日志,确认一切按预期运行
warning : 打印warning,error,critical级别的日志,一个迹象表明,一些意想不到的事情发生了,
          或表明一些问题在不久的将来(例如。磁盘空间低”),这个软件还能按预期工作
error : 打印error,critical级别的日志,更严重的问题,软件没能执行一些功能
critical : 打印critical级别,一个严重的错误,这表明程序本身可能无法继续运行
这时候，如果需要显示低于WARNING级别的内容，可以引入NOTSET级别来显示：

https://www.cnblogs.com/nanyu/articles/10484343.html
https://www.jianshu.com/p/329e4ac2bae4
"""
config = {
    'version': 1,
    'formatters': {
        'simple': {
            'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        },
    },
    'handlers': {
        'mongo': {
            'class': 'log4mongo.handlers.MongoHandler',
            'host': 'localhost',
            'port': 27017,
            'database_name': 'dev_fua',
            'collection': 'exceptionlogs',
            'level': 'DEBUG',
            'username': 'admin',
            'password': '123456',
        },
        'console': {
            'class': 'logging.StreamHandler',
            'level': 'DEBUG', 
            'formatter': 'simple'
        }
    },
    'loggers': { 
        'root': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': True,
        },
        'mongo': {
            'handlers': ['mongo'],
            'level': 'DEBUG',
        }
    }
}

# 记录日志装饰器
def trace_func(func):
    def wrapper(*args, **kargs):
        'Start %s(%s, %s)...' % (func.__name__, args, kargs)
        return func(*args, **kargs)

    return wrapper



def getExceptionLogging(obj):
    logging.config.dictConfig(config)
    logger = logging.getLogger('mongo')
    logger.debug(obj)


def getRequestLogging(obj):
    from app.models.mongodb.logs import Logs
    log=Logs(
        user = obj['user'],
        ip = obj['ip'],
        path = obj['path'],
        host = obj['host'],
        method = obj['method'],
        params = obj['params']
    )
    log.save()
    pass
