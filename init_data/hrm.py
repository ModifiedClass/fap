# -*- coding:utf-8 -*-
# 初始化数据

from app.block.hrm.model import Department


# 初始化部门
def initRootDepartment():
    root = Department()
    root.name='root'
    root.code='root'
    root.type=True
    root.remark='根部门'
    return {'root':root}


def initOneDepartment():
    mz = Department()
    mz.name='测试'
    mz.code='cs'
    mz.type=True
    mz.remark='测试'
    return {'mz':mz}


def initHrmData():
    root = initRootDepartment()
    one = initOneDepartment()
    root['root'].children = [one['mz']]
    return {'hrmData':root['root']}
