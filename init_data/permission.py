# -*- coding:utf-8 -*-
# 权限管理数据
# database:mysql base:fua user:root pwd:123 
from app.block.permission.model import Menu,Rule,Group,User
from init_data.permission_data.user import initUser
from init_data.permission_data.group import initGroup
from init_data.permission_data.rule import initMenuRule,initRuleRule, \
initGroupRule,initUserRule,initDepartmentRule,initTimeLineRule,initJobTypeRule ,\
initJobItemRule,initJobProgrammeRule,initJobAttachmentRule,initJobOperLogRule
from init_data.permission_data.menu import initRootMenu,initPermissionMenu, \
initMenuMenu,initRuleMenu,initGroupMenu,initUserMenu,initDepMenu,initHrmMenu, \
initTtMenu,initTaMenu,initJtMenu,initJiMenu,initJpMenu,initJaMenu,initJoMenu



def initPermissionData():
    # 初始化用户
    users = initUser()
    # 初始化组
    groups = initGroup()
    # 初始化各菜单按钮
    menu_rules = initMenuRule()
    group_rules = initGroupRule()
    rule_rules = initRuleRule()
    user_rules = initUserRule()
    dep_rules = initDepartmentRule()
    tt_rules = initTimeLineRule()
    jt_rules = initJobTypeRule()
    ji_rules = initJobItemRule()
    jp_rules = initJobProgrammeRule()
    ja_rules = initJobAttachmentRule()
    jo_rules = initJobOperLogRule()
    # 初始化菜单
    root_menu = initRootMenu()
    menu_menu = initMenuMenu()
    rule_menu = initRuleMenu()
    group_menu = initGroupMenu()
    user_menu = initUserMenu()
    permission_menu = initPermissionMenu()
    hrm_menu = initHrmMenu()
    dep_menu = initDepMenu()
    # 组添加用户
    groups['admin'].users = [users['Super']]
    groups['guest'].users = [users['Visitor']]
    # 菜单菜单按钮添加组
    menu_rules['add'].groups = [groups['admin']]
    menu_rules['delete'].groups = [groups['admin']]
    menu_rules['edit'].groups = [groups['admin']]
    menu_rules['get'].groups = [groups['admin'],groups['guest']]
    menu_rules['query'].groups = [groups['admin'],groups['guest']]
    # 组菜单按钮添加组
    group_rules['add'].groups = [groups['admin']]
    group_rules['delete'].groups = [groups['admin']]
    group_rules['edit'].groups = [groups['admin']]
    group_rules['get'].groups = [groups['admin'],groups['guest']]
    group_rules['query'].groups = [groups['admin'],groups['guest']]
    group_rules['rules'].groups = [groups['admin'],groups['guest']]
    # 按钮菜单按钮添加组
    rule_rules['add'].groups = [groups['admin']]
    rule_rules['delete'].groups = [groups['admin']]
    rule_rules['edit'].groups = [groups['admin']]
    rule_rules['get'].groups = [groups['admin'],groups['guest']]
    rule_rules['query'].groups = [groups['admin'],groups['guest']]
    # 用户菜单按钮添加组
    user_rules['add'].groups = [groups['admin']]
    user_rules['delete'].groups = [groups['admin']]
    user_rules['edit'].groups = [groups['admin']]
    user_rules['get'].groups = [groups['admin'],groups['guest']]
    user_rules['query'].groups = [groups['admin'],groups['guest']]
    user_rules['groups'].groups = [groups['admin'],groups['guest']]
    # 部门菜单按钮添加组
    dep_rules['add'].groups = [groups['admin']]
    dep_rules['delete'].groups = [groups['admin']]
    dep_rules['edit'].groups = [groups['admin']]
    dep_rules['get'].groups = [groups['admin'],groups['guest']]
    dep_rules['query'].groups = [groups['admin'],groups['guest']]
   
    # 叶子菜单添加按钮
    menu_menu['menu'].rules = [menu_rules['add'],menu_rules['delete'],menu_rules['edit'],menu_rules['get'],menu_rules['query']]
    rule_menu['rule'].rules = [rule_rules['add'],rule_rules['delete'],rule_rules['edit'],rule_rules['get'],rule_rules['query']]
    group_menu['group'].rules = [group_rules['add'],group_rules['delete'],group_rules['edit'],group_rules['get'],group_rules['query'],group_rules['rules']]
    user_menu['user'].rules = [user_rules['add'],user_rules['delete'],user_rules['edit'],user_rules['get'],user_rules['query'],user_rules['groups']]
    dep_menu['department'].rules = [dep_rules['add'],dep_rules['delete'],dep_rules['edit'],dep_rules['get'],dep_rules['query']]
    
    # 菜单添加叶子菜单
    permission_menu['permission'].children = [menu_menu['menu'],rule_menu['rule'],group_menu['group'],user_menu['user']]
    hrm_menu['hrm'].children = [dep_menu['department']]
    task_assessment_menu['task_assessment'].children = [jobtype_menu['jobtype'],jobitem_menu['jobitem'],jobprogramme_menu['jobprogramme'],jobattachment_menu['jobattachment'],joboperlog_menu['joboperlog']]
    # 根菜单添加菜单
    root_menu['root'].children = [hrm_menu['hrm'],timeline_menu['timeline'],permission_menu['permission'],task_assessment_menu['task_assessment']]
    return {'permissionData':root_menu['root']}