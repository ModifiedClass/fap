# -*- coding:utf-8 -*-
# 初始化数据
# database:mysql base:fua user:root pwd:123 

from app import create_app
from app.models.mysql.base import db
# 人事
from init_data.hrm import initHrmData
# 权限
from init_data.permission import initPermissionData


app = create_app()
with app.app_context():
    with db.auto_commit():
        # 初始化数据
        # 权限
        permission_data=initPermissionData()
        db.session.add(permission_data['permissionData'])

        # 人事
        hrm_data = initHrmData()
        db.session.add(hrm_data['hrmData'])

# 运行 python fake.py
