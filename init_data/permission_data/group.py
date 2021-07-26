# -*- coding:utf-8 -*-
# 权限管理数据
# database:mysql base:fua user:root pwd:123 
from app.block.permission.model import Group

# 初始化组
def initGroup():
    g1 = Group()
    g1.name='管理员'
    g1.remark='所有权限'
    g2 = Group()
    g2.name='注册用户'
    g2.remark='基本权限'
    return {'admin':g1,'guest':g2}