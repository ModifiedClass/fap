# -*- coding:utf-8 -*-
import datetime
from flask import current_app
from app.libs.datetime_helper import strptime_to_str



# menu
class MenuViewModel:
    def __init__(self,menu):
        from app.block.permission.model import Menu
        self.id = menu['id']
        self.name=menu['name']
        current_rules=[]
        for rule in menu['rules'].all():
            current_rules.append(dict(rule))
        self.rules=current_rules
        self.create_time=strptime_to_str(menu['create_time'])
        self.remark=menu['remark']
        self.hide_children = menu['hide_children']
        self.hide_self = menu['hide_self']
        self.icon = menu['icon']
        self.path = menu['path']
        self.component = menu['component']
        self.sort = menu['sort']
        self.parent_id = menu['parent_id']
        if menu['parent_id'] != None:
            self.parent_name = Menu.query.filter_by(id=menu['parent_id']).first_or_404().name


class MenuCollection:
    def __init__(self):
        self.total=0
        self.data=[]
        self.success=False
        self.pageNo=1
        self.pageSize=current_app.config['PER_PAGE']
        
    def fill(self,original):
        self.total=original['total']
        self.data=[MenuViewModel(menu) for menu in original['menus']]
        self.success=original['success']
        self.pageNo=original['pageNo'] or 1
        self.pageSize=original['pageSize'] or current_app.config['PER_PAGE']



# rule
class RuleViewModel:
    def __init__(self,rule):
        from app.block.permission.model import Menu
        self.id = rule['id']
        self.name=rule['name']
        self.create_time=strptime_to_str(rule['create_time'])
        self.remark=rule['remark']
        self.api = rule['api']
        self.method = rule['method']
        self.func = rule['func']
        self.menu_id = rule['menu_id']
        if rule['menu_id'] != None:
            self.menu_name = Menu.query.filter_by(id=rule['menu_id']).first_or_404().name
        current_groups=[]
        for group in rule['groups'].all():
            current_groups.append(dict(group))
        self.groups=current_groups



class RuleCollection:
    def __init__(self):
        self.total=0
        self.data=[]
        self.success=False
        self.pageNo=1
        self.pageSize=current_app.config['PER_PAGE']
        
    def fill(self,original):
        self.total=original['total'] or 0
        self.data=[RuleViewModel(rule) for rule in original['rules']]
        self.success=original['success']
        self.pageNo=original['pageNo'] or 1
        self.pageSize=original['pageSize'] or current_app.config['PER_PAGE']



# group
class GroupViewModel:
    def __init__(self,group):
        self.id = group['id']
        self.name=group['name']
        self.create_time=strptime_to_str(group['create_time'])
        self.remark=group['remark']
        current_rules=[]
        ruleids = []
        for rule in group['rules'].all():
            current_rules.append(dict(rule))
            ruleids.append(rule.id)
        self.rules=current_rules
        self.ruleids = ruleids



class GroupCollection:
    def __init__(self):
        self.total=0
        self.data=[]
        self.success=False
        self.pageNo=1
        self.pageSize=current_app.config['PER_PAGE']
        
    def fill(self,original):
        self.total=original['total']
        self.data=[GroupViewModel(group) for group in original['groups']]
        self.success=original['success']
        self.pageNo=original['pageNo'] or 1
        self.pageSize=original['pageSize'] or current_app.config['PER_PAGE']


#user
class UserViewModel:
    def __init__(self,user):
        self.create_time = strptime_to_str(user['create_time'])
        self.last_login_time = strptime_to_str(user['last_login_time'])
        self.id = user['id']
        self.email=user['email']
        self.mobile=user['mobile']
        self.nickname=user['nickname']
        self.realname=user['realname']
        self.gender=user['gender']
        self.id_number=user['id_number']
        self.avatar=user['avatar']
        current_groups=[]
        groupids=[]
        for group in user['groups'].all():
            current_groups.append(dict(group))
            groupids.append(group.id)
        self.groups=current_groups
        self.groupids=groupids
        current_departments=[]
        departmentids=[]
        for department in user['departments'].all():
            current_departments.append(dict(department))
            departmentids.append(department.id)
        self.departments=current_departments
        self.departmentids=departmentids



class UserCollection:
    def __init__(self):
        self.total=0
        self.data=[]
        self.success=False
        self.pageNo=1
        self.pageSize=current_app.config['PER_PAGE']

    # original 原模型数据   
    def fill(self,original):
        self.total=original['total']
        self.data=[UserViewModel(user) for user in original['users']]
        self.success=original['success']
        self.pageNo=original['pageNo'] or 1
        self.pageSize=original['pageSize'] or current_app.config['PER_PAGE']
