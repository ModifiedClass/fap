# -*- coding:utf-8 -*-

from sqlalchemy.orm import backref
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

from app.models.mysql.base import db, Base
from app.libs.error_code import AuthFailed
from app.libs.enums import ClientTypeEnum
from app.libs.datetime_helper import str_to_strptime



# menu 
class Menu(Base):
    __tablename__ = 'fua_menu'
    # __bind_key__ = 'dev_haip'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(30))
    hide_children = db.Column(db.Boolean, default=False)
    hide_self = db.Column(db.Boolean, default=False)
    icon = db.Column(db.String(128))
    path = db.Column(db.String(128))
    component = db.Column(db.String(128))
    sort = db.Column(db.Integer)
    parent_id = db.Column(db.Integer,db.ForeignKey('fua_menu.id', ondelete='CASCADE'))
    children=db.relationship('Menu',lazy='dynamic')
    rules = db.relationship('Rule',backref="menu",lazy='dynamic')

    # 序列化
    def keys(self):
        return ['id', 'name', 'parent_id', 'path', 'component', 'icon', 'hide_children', 'hide_self','sort','remark','create_time']

    def query_conditions(self, kwargs):
        select_uri = [Menu.status == 1]
        if 'name' in kwargs and kwargs['name'] != '':
            select_uri.append(Menu.name.like('%%%s%%' % kwargs['name']))
        if 'remark' in kwargs and kwargs['remark'] != '':
            select_uri.append(Menu.remark.like('%%%s%%' % kwargs['remark']))
        if 'path' in kwargs and kwargs['path'] != '':
            select_uri.append(Menu.path.like('%%%s%%' % kwargs['path']))
        if 'component' in kwargs and kwargs['component'] != '':
            select_uri.append(Menu.component.like('%%%s%%' % kwargs['component']))
        if 'hide_children' in kwargs and kwargs['hide_children'] != '':
            select_uri.append(Menu.hide_children == kwargs['hide_children'])
        if 'hide_self' in kwargs and kwargs['hide_self'] != '':
            select_uri.append(Menu.hide_self == kwargs['hide_self'])    
        if 'parent_id' in kwargs and kwargs['parent_id'] != '':
            select_uri.append(Menu.parent_id == kwargs['parent_id'])

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
            obj = Menu()
            obj.name = newobj['name']
            if 'icon' in newobj:
                obj.icon = newobj['icon']
            if 'path' in newobj:
                obj.path = newobj['path']
            if 'component' in newobj:
                obj.component = newobj['component']
            if 'hide_children' in newobj:
                obj.hide_children = newobj['hide_children']
            if 'hide_self' in newobj:
                obj.hide_self = newobj['hide_self']
            if 'remark' in newobj:
                obj.remark = newobj['remark']
            if 'parent_id' in newobj:
                obj.parent_id = newobj['parent_id']
            if 'sort' in newobj:
                obj.sort = newobj['sort']
            db.session.add(obj)

    @staticmethod
    def update(newobj):
        with db.auto_commit():
            obj = Menu.query.filter_by(id=newobj['id']).first_or_404()
            if 'name' in newobj:
                obj.name = newobj['name']
            if 'icon' in newobj:
                obj.icon = newobj['icon']
            if 'path' in newobj:
                obj.path = newobj['path']
            if 'component' in newobj:
                obj.component = newobj['component']
            if 'hide_children' in newobj:
                obj.hide_children = newobj['hide_children']
            if 'hide_self' in newobj:
                obj.hide_self = newobj['hide_self']
            if 'remark' in newobj:
                obj.remark = newobj['remark']
            if 'parent_id' in newobj:
                obj.parent_id = newobj['parent_id']
            if 'sort' in newobj:
                obj.sort = newobj['sort']
            db.session.add(obj)


# rule 对应前端的按钮
rule_group = db.Table('fua_rule_group',
    db.Column('rule_id',db.Integer, db.ForeignKey('fua_rule.id', ondelete='CASCADE')),
    db.Column('group_id',db.Integer, db.ForeignKey('fua_group.id', ondelete='CASCADE'))
)

class Rule(Base):
    __tablename__ = 'fua_rule'
    # __bind_key__ = 'dev_haip'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(30))
    api = db.Column(db.String(128))
    method = db.Column(db.String(10))
    func = db.Column(db.String(30))
    menu_id = db.Column(db.Integer,db.ForeignKey('fua_menu.id', ondelete='CASCADE'))
    #menu = db.relationship('Menu',backref=db.backref('rules'))
    groups = db.relationship(
        'Group',
        lazy='dynamic',  # 延迟加载
        backref=db.backref(
            'rules',
            lazy='dynamic'  # 延迟加载
        ), secondary='fua_rule_group'  # 指定第三张关联表
    )

    # 序列化
    def keys(self):
        return ['id', 'name', 'api', 'method', 'func', 'remark']

    def query_conditions(self, kwargs):
        select_uri = [Rule.status == 1]
        if 'name' in kwargs and kwargs['name'] != '':
            select_uri.append(Rule.name.like('%%%s%%' % kwargs['name']))
        if 'remark' in kwargs and kwargs['remark'] != '':
            select_uri.append(Rule.remark.like('%%%s%%' % kwargs['remark']))
        if 'api' in kwargs and kwargs['api'] != '':
            select_uri.append(Rule.api.like('%%%s%%' % kwargs['api']))
        if 'method' in kwargs and kwargs['method'] != '':
            select_uri.append(Rule.method.like('%%%s%%' % kwargs['method']))
        if 'menu_id' in kwargs and kwargs['menu_id'] != '':
            select_uri.append(Rule.menu_id == kwargs['menu_id'])

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
            obj = Rule()
            obj.name = newobj['name']
            if 'remark' in newobj:
                obj.remark = newobj['remark']
            if 'api' in newobj:
                obj.api = newobj['api']
            if 'method' in newobj:
                obj.method = newobj['method']
            if 'func' in newobj:
                obj.func = newobj['func']
            if 'menu_id' in newobj:
                obj.menu_id = newobj['menu_id']
            db.session.add(obj)

    @staticmethod
    def update(newobj):
        with db.auto_commit():
            obj = Rule.query.filter_by(id=newobj['id']).first_or_404()
            if 'name' in newobj:
                obj.name = newobj['name']
            if 'remark' in newobj:
                obj.remark = newobj['remark']
            if 'api' in newobj:
                obj.api = newobj['api']
            if 'method' in newobj:
                obj.method = newobj['method']
            if 'func' in newobj:
                obj.func = newobj['func']
            if 'menu_id' in newobj:
                obj.menu_id = newobj['menu_id']
            db.session.add(obj)


# group
user_group = db.Table('fua_user_group',
    db.Column('user_id',db.Integer, db.ForeignKey('fua_user.id', ondelete='CASCADE')),
    db.Column('group_id',db.Integer, db.ForeignKey('fua_group.id', ondelete='CASCADE'))
)

class Group(Base):
    __tablename__ = 'fua_group'
    # __bind_key__ = 'dev_haip'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(24),nullable=False,unique=True)
    users = db.relationship(
        'User',
        lazy='dynamic',  # 延迟加载
        backref=db.backref(
            'groups',
            lazy='dynamic'  # 延迟加载
        ),
        secondary='fua_user_group'  # 指定第三张关联表
    )

    # 序列化
    def keys(self):
        return ['id', 'name', 'remark']

    def query_conditions(self, kwargs):
        select_uri = [Group.status == 1]
        if 'name' in kwargs and kwargs['name'] != '':
            select_uri.append(Group.name.like('%%%s%%' % kwargs['name']))

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
            obj = Group()
            obj.name = newobj['name']
            if 'remark' in newobj:
                obj.remark = newobj['remark']
            if 'ruleids' in newobj:
                from app.block.permission.model import Rule
                arr = []
                for id in newobj['ruleids']:
                    arr.append(Rule.query.filter_by(id=id).first_or_404())
                obj.rule = arr
            db.session.add(obj)

    @staticmethod
    def update(newobj):
        with db.auto_commit():
            obj = Group.query.filter_by(id=newobj['id']).first_or_404()
            if 'name' in newobj:
                obj.name = newobj['name']
            if 'remark' in newobj:
                obj.remark = newobj['remark']
            if 'ruleids' in newobj and newobj['ruleids'] != None:
                from app.block.permission.model import Rule
                rarr = []
                for id in newobj['ruleids']:
                    rarr.append(Rule.query.filter_by(id=id).first_or_404())
                obj.rules = rarr
            db.session.add(obj)


# user
class User(Base):
    __tablename__ = 'fua_user'
    # __table_args__ = {'autoload': True}
    # __bind_key__ = 'dev_fua'  # 多实例配置在此处执行即可
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(24), unique=True)
    mobile = db.Column(db.String(24), unique=True)
    nickname = db.Column(db.String(24), unique=True)
    _password = db.Column('password', db.String(128))
    last_login_time = db.Column(db.Integer)
    realname = db.Column(db.String(24))
    gender = db.Column(db.Integer,  default=1)
    id_number = db.Column(db.String(20))
    avatar = db.Column(db.String(256))


    # 用户序列化
    def keys(self):
        return ['id', 'email', 'mobile', 'nickname', 'last_login_time', \
            'realname', 'gender', 'id_number', 'avatar', 'remark']

    @property
    def password(self):
        return self._password

    @password.setter
    def password(self, raw):
        self._password = generate_password_hash(raw)

    @property
    def last_login_datetime(self):
        if self.last_login_time:
            return datetime.fromtimestamp(self.last_login_time)
        else:
            return datetime.now().timestamp()

    @staticmethod
    def register_by_email(account, secret):
        with db.auto_commit():
            # 对象下创建对象本身，需设置为静态方法
            user = User()
            user.email = account
            user.password = secret
            db.session.add(user)

    @staticmethod
    def register_by_mobile(mobile, secret):
        with db.auto_commit():
            # 对象下创建对象本身，需设置为静态方法
            user = User()
            user.mobile = mobile
            user.password = secret
            db.session.add(user)

    @staticmethod
    def register_by_username(nickname, secret):
        with db.auto_commit():
            # 对象下创建对象本身，需设置为静态方法
            user = User()
            user.nickname = nickname
            user.password = secret
            db.session.add(user)

    @staticmethod
    def verify(client_type, account, password):
        if client_type == ClientTypeEnum.USER_EMAIL:
            user = User.query.filter_by(email=account).first_or_404()
        elif client_type == ClientTypeEnum.USER_MOBILE:
            user = User.query.filter_by(mobile=account).first_or_404()
        elif client_type == ClientTypeEnum.USER_NICKNAME:
            user = User.query.filter_by(nickname=account).first_or_404()
        else:
            raise AuthFailed()

        if not user.check_password(password):
            raise AuthFailed()
        current_rules=[] #['endpiont1','endpoint2']
        if len(user.groups.all()) > 0:
            temp=[]
            for sc in user.groups.all():
                for aa in sc.rules.all():
                    temp.append(aa.func)
            current_rules =list(set(temp))
        return {'uid': user.id,'rules':current_rules}

    def check_password(self, raw):
        if not self._password:
            return False
        # generate_password_hash 加密 check_password_hash对比加密后是否一致
        return check_password_hash(self._password, raw)

    def query_conditions(self, kwargs):
        select_uri = [User.status == 1]
        if 'email' in kwargs and kwargs['email'] != '':
            select_uri.append(User.email.like('%%%s%%' % kwargs['email']))
        if 'mobile' in kwargs and kwargs['mobile'] != '':
            select_uri.append(User.mobile.like('%%%s%%' % kwargs['mobile']))
        if 'nickname' in kwargs and kwargs['nickname'] != '':
            select_uri.append(User.nickname.like('%%%s%%' % kwargs['nickname']))
        if 'realname' in kwargs and kwargs['realname'] != '':
            select_uri.append(User.realname.like('%%%s%%' % kwargs['realname']))
        if 'gender' in kwargs and kwargs['gender'] != '':
            select_uri.append(User.gender == kwargs['gender'])
        if 'id_number' in kwargs and kwargs['id_number'] != '':
            select_uri.append(User.id_number.like('%%%s%%' % kwargs['id_number']))
        if 'create_time_start' in kwargs and kwargs['create_time_start'] != '' and \
        'create_time_end' in kwargs and kwargs['create_time_end'] != '':
            start = str_to_strptime(kwargs['create_time_start'])
            end = str_to_strptime(kwargs['create_time_end'])
            select_uri.append(User.create_time.between(start,end))
            
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
            obj = User()
            obj.last_login_time = int(datetime.now().timestamp())
            if 'mobile' in newobj:
                obj.mobile = newobj['mobile']
            if 'email' in newobj:
                obj.email = newobj['email']
            if 'nickname' in newobj:
                obj.nickname = newobj['nickname']
            if 'realname' in newobj:
                obj.realname = newobj['realname']
            if 'gender' in newobj:
                obj.gender = newobj['gender']
            if 'id_number' in newobj:
                obj.id_number = newobj['id_number']
            if 'password' in newobj and newobj['password'] != None:
                obj.password = newobj['password']
            if 'remark' in newobj:
                obj.remark = newobj['remark']
            if 'avatar' in newobj:
                obj.avatar = newobj['avatar']
            db.session.add(obj)

    @staticmethod
    def update(newobj):
        with db.auto_commit():
            obj = User.query.filter_by(id=newobj['id']).first_or_404()
            if 'mobile' in newobj:
                obj.mobile = newobj['mobile']
            if 'email' in newobj:
                obj.email = newobj['email']
            if 'nickname' in newobj:
                obj.nickname = newobj['nickname']
            if 'realname' in newobj:
                obj.realname = newobj['realname']
            if 'gender' in newobj:
                obj.gender = newobj['gender']
            if 'id_number' in newobj:
                obj.id_number = newobj['id_number']
            if 'password' in newobj and newobj['password'] != None:
                obj.password = newobj['password']
            if 'remark' in newobj:
                obj.remark = newobj['remark']
            if 'avatar' in newobj:
                obj.avatar = newobj['avatar']
            if 'last_login_time' in newobj:
                obj.last_login_time = int(datetime.now().timestamp())
            if 'groupids' in newobj and newobj['groupids'] != None:
                from app.block.permission.model import Group
                garr = []
                for id in newobj['groupids']:
                    garr.append(Group.query.filter_by(id=id).first_or_404())
                obj.groups = garr
            if 'departmentids' in newobj and newobj['departmentids'] != None:
                from app.block.hrm.model import Department
                darr = []
                for id in newobj['departmentids']:
                    darr.append(Department.query.filter_by(id=id).first_or_404())
                obj.departments = darr
            db.session.add(obj)
