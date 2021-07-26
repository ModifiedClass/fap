# -*- coding:utf-8 -*-
from flask import current_app
from app.libs.datetime_helper import strptime_to_str


class DepartmentViewModel:
    def __init__(self,department):
        from app.block.hrm.model import Department
        self.id = department['id']
        self.code = department['code']
        self.name=department['name']
        self.parent_id=department['parent_id']
        if department['parent_id'] != None:
            self.parent_name = Department.query.filter_by(id=department['parent_id']).first_or_404().name
        self.type=department['type']
        self.create_time=strptime_to_str(department['create_time'])
        self.remark=department['remark']



class DepartmentCollection:
    def __init__(self):
        self.total=0
        self.data=[]
        
    def fill(self,original):
        self.total=original['total']
        self.data=[DepartmentViewModel(department) for department in original['departments']]
        self.success=original['success']
        self.pageNo=original['pageNo'] or 1
        self.pageSize=original['pageSize'] or current_app.config['PER_PAGE']
