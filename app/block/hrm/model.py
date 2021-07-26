# -*- coding:utf-8 -*-

from app.models.mysql.base import db, Base
from app.block.permission.model import User


# department
user_department = db.Table('fua_user_department',
    db.Column('user_id',db.Integer, db.ForeignKey('fua_user.id', ondelete='CASCADE')),
    db.Column('department_id',db.Integer, db.ForeignKey('fua_department.id', ondelete='CASCADE'))
)

class Department(Base):
    __tablename__ = 'fua_department'
    # __bind_key__ = 'dev_haip'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(24))
    code = db.Column(db.String(24))
    type = db.Column(db.Boolean())
    parent_id = db.Column(db.Integer,db.ForeignKey('fua_department.id', ondelete='CASCADE'))
    children=db.relationship('Department')
    users = db.relationship(
        'User',
        lazy='dynamic',  # 延迟加载
        backref=db.backref(
            'departments',
            lazy='dynamic'  # 延迟加载
        ), secondary='fua_user_department'  # 指定第三张关联表
    )

    # 序列化
    def keys(self):
        return ['id', 'name', 'code', 'parent_id']

    def query_conditions(self, kwargs):
        select_uri = [Department.status == 1]
        if 'name' in kwargs and kwargs['name'] != '':
            select_uri.append(Department.name.like('%%%s%%' % kwargs['name']))
        if 'code' in kwargs and kwargs['code'] != '':
            select_uri.append(Department.code.like('%%%s%%' % kwargs['code']))
        if 'parent_id' in kwargs and kwargs['parent_id'] != '':
            select_uri.append(Department.parent_id == kwargs['parent_id'])
        if 'type' in kwargs and kwargs['type'] != '':
            select_uri.append(Department.type == kwargs['type'])

        total = len(self.query.filter(*select_uri).all())
        if 'ispage' in kwargs and kwargs['ispage']==True:
            limit=int(kwargs['pageSize'])
            offset=(int(kwargs['pageNo'])-1)*int(kwargs['pageSize'])
            result = self.query.filter(*select_uri).offset(offset).limit(limit).all()
        else:
            result = self.query.filter(*select_uri).all()
        return {'data':result,'total':total}
    
    @staticmethod
    def create(newobj):
        with db.auto_commit():
            # 对象下创建对象本身，需设置为静态方法
            obj = Department()
            obj.name = newobj['name']
            if 'remark' in newobj:
                obj.remark = newobj['remark']
            if 'code' in newobj:
                obj.code = newobj['code']
            if 'parent_id' in newobj:
                obj.parent_id = newobj['parent_id']
            if 'type' in newobj:
                obj.type = newobj['type']
            db.session.add(obj)

    @staticmethod
    def update(newobj):
        with db.auto_commit():
            obj = Department.query.filter_by(id=newobj['id']).first_or_404()
            if 'name' in newobj:
                obj.name = newobj['name']
            if 'remark' in newobj:
                obj.remark = newobj['remark']
            if 'code' in newobj:
                obj.code = newobj['code']
            if 'parent_id' in newobj:
                obj.parent_id = newobj['parent_id']
            if 'type' in newobj:
                obj.type = newobj['type']
            db.session.add(obj)
