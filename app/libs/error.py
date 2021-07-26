# -*- coding:utf-8 -*-

from flask import request, json
from werkzeug.exceptions import HTTPException


class APIException(HTTPException):
    code = 500
    msg = 'sorry, we make a mistake o(╥﹏╥)o!'
    error_code = 999

    def __init__(self, msg=None, code=None, error_code=None, headers=None):
        if code:
            self.code = code
        if error_code:
            self.error_code = error_code
        if msg:
            self.msg = msg
        super(APIException, self).__init__(msg, None)

    def get_body(self, environ=None, scope=None):
        # 重写 原get_body返回的是html
        body = dict(
            msg=self.msg,
            error_code=self.error_code,
            # 当前请求的方法+当前请求的url
            request=request.method + ' ' + self.get_url_no_param()
        )
        text = json.dumps(body)
        return text

    @staticmethod
    def get_headers(self, environ=None):
        """Get a list of headers."""
        return [('Content-Type', 'application/json')]

    @staticmethod
    def get_url_no_param():
        full_path = str(request.full_path)
        main_path = full_path.split('?')
        return main_path[0]