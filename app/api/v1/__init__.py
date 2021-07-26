# -*- coding:utf-8 -*-

from flask import Blueprint
from app.api.v1 import file,antd
from app.api.v1 import verification_code, token
from app.block.hrm import api as hrm
from app.block.permission import api as permission

def create_blueprint_v1():
    # 创建蓝图对象
    bp_v1 = Blueprint('v1', __name__)

    # 红图向蓝图的注册 # user.api 红图对象
    # url_prefix='/user' 红图函数增加判断url_prefix = '/' + self.name，可以不用添加此字段

    token.api.register(bp_v1, url_prefix='/token')
    verification_code.api.register(bp_v1)
    file.api.register(bp_v1)

    hrm.department_api.register(bp_v1)
    
    permission.auth_api.register(bp_v1)
    permission.rule_api.register(bp_v1)
    permission.menu_api.register(bp_v1)
    permission.group_api.register(bp_v1)
    permission.user_api.register(bp_v1)

    antd.antd_api.register(bp_v1)
    return bp_v1
