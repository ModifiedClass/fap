from flask import request
from wtforms import Form, IntegerField, StringField, Field
from wtforms.validators import ValidationError

from app.libs.error_code import ParamException


class BaseFrom(Form):
    id = IntegerField()
    remark = StringField()

    def __init__(self):
        data = request.get_json(silent=True)
        args = request.args.to_dict()
        super(BaseFrom, self).__init__(data=data, **args)

    def validate_for_api(self):
        valid = super(BaseFrom, self).validate()
        if not valid:
            # form errors
            raise ParamException(msg=self.errors)
        return self


# 自定义列表字段
class ListField(Field):

    def process_formdata(self, valuelist):
        try:
            if valuelist[0] and isinstance(valuelist[0], list):
                self.data = valuelist[0]
            else:
                raise ValidationError('list validate error')
        except:
            raise ValidationError('list validate error, exception')
