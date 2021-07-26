# -*- coding:utf-8 -*-

from flask import request,g
from werkzeug.exceptions import HTTPException
from app.libs.error_code import APIException
from app.libs.error_code import ServerError
from app.libs.log import getRequestLogging
from app.libs.log import getExceptionLogging,getRequestLogging

def load_middleware(app):
    # 全局请求拦截器
    @app.before_request
    def before():
        print('before')
        getRequestLogging({
            #'user': g.user.uid if g.user else '',
            'user':'',
            'path':request.path,
            'host':request.url,
            'ip':request.environ.get('HTTP_X_REAL_IP', request.remote_addr),
            'method':request.method,
            'params':str(request.values)
        })
        pass

    @app.after_request
    def after(resp):
        print('resp')
        return resp
    

    # flask1.0才支持errorhandler HTTPException
    #全局异常处理
    @app.errorhandler(Exception)
    def framework_error(e):
        print(e)
        if isinstance(e, APIException):
            getExceptionLogging(e)
            return e
        if isinstance(e, HTTPException):
            code = e.code
            msg = e.description
            error_code = 1007
            getExceptionLogging(APIException(msg, code, error_code))
            return APIException(msg, code, error_code)
        else:
            # 调试模式
            if not app.config['DEBUG']:
                getExceptionLogging(ServerError())
                return ServerError()
            else:
                # 如果是调试模式，就抛出原型异常
                raise e