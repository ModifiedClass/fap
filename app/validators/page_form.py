from wtforms import IntegerField,BooleanField
from wtforms.validators import DataRequired,Regexp

from app.validators.base import BaseFrom as Form


class PageSearchForm(Form):
    ispage = BooleanField()
    """ pageNo=IntegerField(validators=[
        DataRequired(),
        Regexp(r'^\d+$')])
    pageSize=IntegerField(validators=[
        DataRequired(),
        Regexp(r'^[1-9]\d*$')]) """
    pageNo=IntegerField()
    pageSize=IntegerField()
    success=BooleanField()