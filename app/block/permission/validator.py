# -*- coding:utf-8 -*-

from wtforms import StringField, IntegerField, BooleanField,DateTimeField
from wtforms import ValidationError
from wtforms.validators import DataRequired, length, Email, Regexp

from app.validators.base import BaseFrom as Form
from app.validators.page_form import PageSearchForm
from app.block.permission.model import Group,Rule,Menu,User
from app.libs.enums import ClientTypeEnum


class IdsForm(Form):
    ids=StringField()



# rule
class RuleUpdateForm(Form):
    name = StringField(validators=[DataRequired(message='不允许为空'), length(min=2, max=10)])
    api = StringField()
    method = StringField()
    func = StringField()
    menu_id = IntegerField()


class RuleInsertForm(RuleUpdateForm):
    # 验证是否存在
    def validate_name(self, value):
        if Rule.query.filter_by(name=value.data).first():
            raise ValidationError()


class RuleGetForm(Form):
    name = StringField()
    menu_id = IntegerField()


class RuleSearchForm(PageSearchForm):
    name=StringField()
    api = StringField()
    method = StringField()
    func = StringField()
    menu_id = IntegerField()


class RuleDeleteForm(Form):
    pass



# menu
class MenuUpdateForm(Form):
    name = StringField(validators=[DataRequired(message='不允许为空'), length(min=2, max=32)])
    hide_children = BooleanField()
    hide_self = BooleanField()
    icon = StringField()
    path = StringField()
    component = StringField()
    sort = IntegerField()
    parent_id = IntegerField()


class MenuInsertForm(MenuUpdateForm):
    # 验证是否存在
    def validate_name(self, value):
        if Menu.query.filter_by(name=value.data).first():
            raise ValidationError()


class MenuGetForm(Form):
    name = StringField()
    remark = StringField()
    path = StringField()
    component = StringField()
    sort = IntegerField()
    parent_id = IntegerField()


class MenuSearchForm(PageSearchForm):
    name=StringField()
    remark = StringField()
    path = StringField()
    component = StringField()
    sort = IntegerField()
    parent_id = IntegerField()
    hide_children = BooleanField()
    hide_self = BooleanField()


class MenuDeleteForm(Form):
    pass



# group
class GroupUpdateForm(Form):
    name = StringField(validators=[DataRequired(message='不允许为空'), length(min=2, max=32)])


class GroupInsertForm(GroupUpdateForm):
    # 验证是否存在
    def validate_name(self, value):
        if Group.query.filter_by(name=value.data).first():
            raise ValidationError()


class GroupGetForm(Form):
    name = StringField()


class GroupSearchForm(PageSearchForm):
    name=StringField()


class GroupDeleteForm(Form):
    pass



# user
class UserUpdateForm(Form):
    nickname = StringField(validators=[DataRequired(message='不允许为空'), length(min=2, max=32)])
    email=StringField()
    mobile=StringField()
    realname=StringField()
    password=StringField()
    gender=IntegerField()
    id_number=StringField()
    avatar=StringField()
    last_login_time=IntegerField()
    groupids=StringField()
    departmentids=StringField()


class UserInsertForm(UserUpdateForm):
    # 验证是否存在
    def validate_name(self, value):
        if User.query.filter_by(nickname=value.data).first():
            raise ValidationError()


class UserGetForm(Form):
    nickname = StringField()
    email=StringField()
    mobile=StringField()
    realname=StringField()
    gender=IntegerField()
    id_number=StringField()


class UserSearchForm(PageSearchForm):
    nickname = StringField()
    email=StringField()
    mobile=StringField()
    realname=StringField()
    gender=IntegerField()
    id_number=StringField()
    create_time_start=DateTimeField()
    create_time_end=DateTimeField()


class UserDeleteForm(Form):
    pass


class UserResetPasswordForm(Form):
    password=StringField()


class ClientForm(Form):
    # 帐号验证
    account = StringField(validators=[DataRequired(message='不允许为空'), length(min=2, max=32)])
    # 密码验证 不必须，token验证不需要密码
    secret = StringField()
    # 帐户类型 邮箱 手机 微信等
    type = IntegerField(validators=[DataRequired()])

    # 自定义验证 必须是枚举中的值
    def validate_type(self, value):
        try:
            # 验证值 数字类型转换枚举
            client = ClientTypeEnum(value.data)
        except ValueError as e:
            raise e
        self.type.data = client


class UserEmailForm(ClientForm):
    account = StringField(validators=[
        Email(message='invalidate email')
    ])
    secret = StringField(validators=[
        DataRequired(),
        # password can only include letters , numbers and "_"
        Regexp(r'^[A-Za-z0-9_*&$#@]{6,22}$')
    ])

    # 验证用户是否存在
    def validate_account(self, value):
        if User.query.filter_by(email=value.data).first():
            raise ValidationError()


class UserMobileForm(ClientForm):
    account = StringField(validators=[
        DataRequired(),
        Regexp(r'1[34578]\d{9}')])
    secret = StringField(validators=[
        DataRequired(),
        # password can only include letters , numbers and "_"
        Regexp(r'^[A-Za-z0-9_*&$#@]{6,22}$')
    ])

    # 验证用户是否存在
    def validate_mobile(self, value):
        if User.query.filter_by(mobile=value.data).first():
            raise ValidationError()


class UserNickNameForm(ClientForm):
    secret = StringField(validators=[
        DataRequired(),
        # password can only include letters , numbers and "_"
        Regexp(r'^[A-Za-z0-9_*&$#@]{6,22}$')
    ])
    account = StringField(validators=[DataRequired(), length(min=2, max=22)])

    # 验证用户是否存在
    def validate_nickname(self, value):
        if User.query.filter_by(nickname=value.data).first():
            raise ValidationError()


class TokenForm(Form):
    token = StringField(validators=[DataRequired()])


class UidForm(Form):
    uid = IntegerField()