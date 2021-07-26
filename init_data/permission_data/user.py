# -*- coding:utf-8 -*-
# 权限管理数据
# database:mysql base:fua user:root pwd:123 
from app.block.permission.model import User


# 初始化用户
def initUser():
    u1 = User()
    u1.nickname = 'Super'
    u1.realname = '管理员'
    u1.password = '123456'
    u1.email = '***@qq.com'
    u1.mobile = '***'
    u2 = User()
    u2.nickname = 'Visitor'
    u2.realname = '访客'
    u2.password = '123456'
    u2.email = 'visitor@qq.com'
    u2.mobile = '***'
    return {'Super':u1,'Visitor':u2}

