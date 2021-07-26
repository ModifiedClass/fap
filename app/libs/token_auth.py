# -*- coding:utf-8 -*-

from flask import current_app, g, request
from flask_httpauth import HTTPBasicAuth
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer, BadSignature, SignatureExpired
from collections import namedtuple

from app.libs.error_code import AuthFailed, Forbidden
from app.libs.rule import verify_rule

auth = HTTPBasicAuth()
# nametuple可以使用g.User.uid而不必g.User['uid']
User = namedtuple('User', ['uid', 'ac_type', 'rules'])


@auth.verify_password
def verify_password(token, password):
    # token
    # HTTP 账号密码 flask_httpauth要求在header中发送账号密码
    # header key:value   key = Authorization  value = 账号:密码   value = basic base64(账号:密码)
    ##1 postman->headers->key:authorization value:basic base64(u: p) ->send
    ##2 postman->Authorization->type:Basic Auth username:token ->send
    # 前端ruquest拦截 headers:{Authorization:'Basic ' + btoa(getToken() + ":")}
    user_info = verify_auth_token(token)
    if not user_info:
        return False
    else:
        # 用户信息存在g中
        g.user = user_info
        return True


def verify_auth_token(token):
    s = Serializer(current_app.config['SECRET_KEY'])
    try:
        data = s.loads(token)
    except BadSignature:
        raise AuthFailed(msg='token is invalid', error_code=1002)
    except SignatureExpired:
        raise AuthFailed(msg='token is expired', error_code=1003)
    uid = data['uid']
    ac_type = data['type']
    rules = data['rules']
    # request 视图函数
    allow = verify_rule(rules, request.endpoint)
    if not allow:
        raise Forbidden()
    return User(uid, ac_type, rules)
