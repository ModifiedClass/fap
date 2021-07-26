# -*- coding:utf-8 -*-
# 权限管理数据
# database:mysql base:fua user:root pwd:123 
from app.block.permission.model import Rule

# 初始化菜单菜单操作规则
def initMenuRule():
    mr1 = Rule()
    mr1.name='addmenu'
    mr1.remark='新建菜单'
    mr1.api='/permission/menu'
    mr1.func='menu_post'
    mr1.method='post'
    mr2 = Rule()
    mr2.name='deletemenu'
    mr2.remark='删除菜单'
    mr2.api='/permission/menu'
    mr2.func='menu_delete'
    mr2.method='delete'
    mr3 = Rule()
    mr3.name='editmenu'
    mr3.remark='编辑菜单'
    mr3.api='/permission/menu'
    mr3.func='menu_put'
    mr3.method='put'
    mr4 = Rule()
    mr4.name='getmenu'
    mr4.remark='菜单详情'
    mr4.api='/permission/menu'
    mr4.func='menu_get'
    mr4.method='get'
    mr5 = Rule()
    mr5.name='querymenu'
    mr5.remark='查询菜单'
    mr5.api='/permission/menu/collection'
    mr5.func='menu_query'
    mr5.method='get'
    return {'add':mr1,'delete':mr2,'edit':mr3,'get':mr4,'query':mr5}


# 初始化规则菜单操作规则
def initRuleRule():
    # rule-rule
    rr1 = Rule()
    rr1.name='addrule'
    rr1.remark='新建规则'
    rr1.api='/permission/rule'
    rr1.func='rule_post'
    rr1.method='post'

    rr2 = Rule()
    rr2.name='deleterule'
    rr2.remark='删除规则'
    rr2.api='/permission/rule'
    rr2.func='rule_delete'
    rr2.method='delete'

    rr3 = Rule()
    rr3.name='editrule'
    rr3.remark='编辑规则'
    rr3.api='/permission/rule'
    rr3.func='rule_put'
    rr3.method='put'

    rr4 = Rule()
    rr4.name='getrule'
    rr4.remark='规则详情'
    rr4.api='/permission/rule'
    rr4.func='rule_get'
    rr4.method='get'

    rr5 = Rule()
    rr5.name='queryrule'
    rr5.remark='查询规则'
    rr5.api='/permission/rule/collection'
    rr5.func='rule_query'
    rr5.method='get'
    return {'add':rr1,'delete':rr2,'edit':rr3,'get':rr4,'query':rr5}


# 初始化组菜单操作规则
def initGroupRule():
    # rule-group
    gr1 = Rule()
    gr1.name='addgroup'
    gr1.remark='新建组'
    gr1.api='/permission/group'
    gr1.func='group_post'
    gr1.method='post'

    gr2 = Rule()
    gr2.name='deletegroup'
    gr2.remark='删除组'
    gr2.api='/permission/group'
    gr2.func='group_delete'
    gr2.method='delete'

    gr3 = Rule()
    gr3.name='editgroup'
    gr3.remark='编辑组'
    gr3.api='/permission/group'
    gr3.func='group_put'
    gr3.method='put'

    gr4 = Rule()
    gr4.name='getgroup'
    gr4.remark='组详情'
    gr4.api='/permission/group'
    gr4.func='group_get'
    gr4.method='get'

    gr5 = Rule()
    gr5.name='querygroup'
    gr5.remark='查询组'
    gr5.api='/permission/group/collection'
    gr5.func='group_query'
    gr5.method='get'

    gr6 = Rule()
    gr6.name='grouprules'
    gr6.remark='组授权'
    gr6.api='/permission/group/rules'
    gr6.func='group_rules'
    gr6.method='put'
    return {'add':gr1,'delete':gr2,'edit':gr3,'get':gr4,'query':gr5,'rules':gr6}


# 初始化用户菜单操作规则
def initUserRule():
    # rule-user
    ur1 = Rule()
    ur1.name='adduser'
    ur1.remark='新建用户'
    ur1.api='/permission/user'
    ur1.func='user_post'
    ur1.method='post'

    ur2 = Rule()
    ur2.name='deleteuser'
    ur2.remark='删除用户'
    ur2.api='/permission/user'
    ur2.func='user_delete'
    ur2.method='delete'

    ur3 = Rule()
    ur3.name='edituser'
    ur3.remark='编辑用户'
    ur3.api='/permission/user'
    ur3.func='user_put'
    ur3.method='put'

    ur4 = Rule()
    ur4.name='getuser'
    ur4.remark='用户详情'
    ur4.api='/permission/user'
    ur4.func='user_get'
    ur4.method='get'

    ur5 = Rule()
    ur5.name='queryuser'
    ur5.remark='查询用户'
    ur5.api='/permission/user/collection'
    ur5.func='user_query'
    ur5.method='get'

    ur6 = Rule()
    ur6.name='usergroups'
    ur6.remark='用户分组'
    ur6.api='/permission/user/groups'
    ur6.func='user_groups'
    ur6.method='put'
    return {'add':ur1,'delete':ur2,'edit':ur3,'get':ur4,'query':ur5,'groups':ur6}


# 初始化部门菜单操作规则
def initDepartmentRule():
    # rule-department
    dr1 = Rule()
    dr1.name='adddepartment'
    dr1.remark='新建部门'
    dr1.api='/hrm/department'
    dr1.func='department_post'
    dr1.method='post'

    dr2 = Rule()
    dr2.name='deletedepartment'
    dr2.remark='删除部门'
    dr2.api='/hrm/department'
    dr2.func='department_delete'
    dr2.method='delete'

    dr3 = Rule()
    dr3.name='editdepartment'
    dr3.remark='编辑部门'
    dr3.api='/hrm/department'
    dr3.func='department_put'
    dr3.method='put'

    dr4 = Rule()
    dr4.name='getdepartment'
    dr4.remark='部门详情'
    dr4.api='/hrm/department'
    dr4.func='department_get'
    dr4.method='get'

    dr5 = Rule()
    dr5.name='querydepartment'
    dr5.remark='查询部门'
    dr5.api='/hrm/department/collection'
    dr5.func='department_query'
    dr5.method='get'
    return {'add':dr1,'delete':dr2,'edit':dr3,'get':dr4,'query':dr5}


