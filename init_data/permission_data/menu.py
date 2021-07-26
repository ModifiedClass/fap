# -*- coding:utf-8 -*-
# 权限管理数据
# database:mysql base:fua user:root pwd:123 
from app.block.permission.model import Menu

# 初始化根菜单
def initRootMenu():
    m0 = Menu()
    m0.remark='根菜单'
    m0.name='root'
    m0.path='/'
    m0.sort=0
    return {'root':m0}


# 初始化权限菜单
def initPermissionMenu():
    m1 = Menu()
    m1.remark='用户访问站点的权限分配等'
    m1.name='权限'
    m1.path='/permission'
    m1.icon='icon-key'
    m1.sort=99
    return {'permission':m1}


# 初始化菜单菜单
def initMenuMenu():
    m2=Menu()
    m2.remark='menu'
    m2.name='菜单'
    m2.path='/permission/menu'
    m2.icon='icon-menu'
    m2.component='/permission/Menu'
    m2.sort = 1
    return {'menu':m2}


# 初始化规则菜单
def initRuleMenu():
    m3=Menu()
    m3.remark='按钮'
    m3.name='规则'
    m3.path='/permission/rule'
    m3.icon='icon-deploymentunit'
    m3.component='/permission/Rule'
    m3.sort = 2
    return {'rule':m3}


# 初始化组菜单
def initGroupMenu():
    m4=Menu()
    m4.remark='角色'
    m4.name='分组'
    m4.icon='icon-team'
    m4.path='/permission/group'
    m4.component='/permission/Group'
    m4.sort = 3
    return {'group':m4}


# 初始化用户菜单
def initUserMenu():
    m5=Menu()
    m5.remark='user'
    m5.name='用户'
    m5.path='/permission/user'
    m5.icon='icon-user'
    m5.component='/permission/User'
    m5.sort = 4
    return {'user':m5}


# 初始化部门菜单
def initDepMenu():
    m6=Menu()
    m6.remark='department'
    m6.name='部门'
    m6.path='/hrm/department'
    m6.icon='icon-cluster'
    m6.component='/hrm/Department'
    m6.sort = 4
    return {'department':m6}


# 初始化人事菜单
def initHrmMenu():
    m7 = Menu()
    m7.remark='hrm'
    m7.name='人事'
    m7.path='/hrm'
    m7.icon='icon-contacts'
    m7.sort=1
    return {'hrm':m7}


