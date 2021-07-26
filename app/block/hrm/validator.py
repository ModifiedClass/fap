# -*- coding:utf-8 -*-

from sqlalchemy.sql.sqltypes import Boolean
from wtforms import StringField,IntegerField
from wtforms import ValidationError
from wtforms.fields.core import BooleanField
from wtforms.validators import DataRequired, length

from app.validators.base import BaseFrom as Form
from app.validators.page_form import PageSearchForm
from app.block.hrm.model import Department



# department
class DepartmentUpdateForm(Form):
    name = StringField(validators=[DataRequired(message='不允许为空'), length(min=2, max=32)])
    code = StringField(validators=[DataRequired(message='不允许为空'), length(min=2, max=32)])
    parent_id = IntegerField()
    type = BooleanField()


class DepartmentInsertForm(DepartmentUpdateForm):
    # 验证是否存在
    def validate_name(self, value):
        if Department.query.filter_by(name=value.data).first():
            raise ValidationError()


class DepartmentGetForm(Form):
    name = StringField()


class DepartmentSearchForm(PageSearchForm):
    name=StringField()
    code = StringField()
    parent_id = IntegerField()
    type = BooleanField()


class DepartmentDeleteForm(Form):
    pass
