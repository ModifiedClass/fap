# -*- coding:utf-8 -*-

from sqlalchemy.sql.expression import true
from app.libs.redprint import Redprint
from app.libs.token_auth import auth
from app.block.hrm.validator import DepartmentInsertForm, DepartmentGetForm, DepartmentSearchForm, DepartmentDeleteForm,DepartmentUpdateForm
from app.block.hrm.view_model import DepartmentCollection
from app.block.hrm.services import department_edit as sdepartment_edit,department_delete as sdepartment_delete ,\
department_get as sdepartment_get,department_query as sdepartment_query

# department
department_api = Redprint('department')

@department_api.route('', methods=['POST'])
@auth.login_required
def department_post():
    return sdepartment_edit(DepartmentInsertForm().validate_for_api())

@department_api.route('', methods=['DELETE'])
@auth.login_required
def department_delete():
    return sdepartment_delete(DepartmentDeleteForm().validate_for_api())

@department_api.route('', methods=['PUT'])
@auth.login_required
def department_put():
    return sdepartment_edit(DepartmentUpdateForm().validate_for_api())


@department_api.route('', methods=['GET'])
@auth.login_required
def department_get():
    return sdepartment_get(DepartmentGetForm())


@department_api.route('/collection', methods=['GET'])
@auth.login_required
def department_query():
    return sdepartment_query(DepartmentSearchForm(),DepartmentCollection())