# -*- coding:utf-8 -*-

from flask import jsonify,json
from app.libs.error_code import DeleteSuccess,Success
from app.block.hrm.model import Department

# department

def department_edit(form):
    obj = {
        'id':form.id.data,
        'name':form.name.data,
        'code':form.code.data,
        'parent_id':form.parent_id.data,
        'type':form.type.data,
        'remark':form.remark.data
    }
    if form.id.data != None and form.id.data != '':
        Department.update(obj)
    else:
        Department.create(obj)
    return Success()


def department_delete(form):
    id = form.id.data
    obj = Department.query.filter_by(id=id).first_or_404()
    obj.delete()   # 软删除 更改数据库状态
    return DeleteSuccess()


def department_get(form):
    if form.validate_for_api():
        obj = Department.query.filter_by(id=form.id.data).first_or_404()
    return jsonify(obj)


def department_query(form,objs):
    if form.validate_for_api():
        kwargs = {
            'ispage':form.ispage.data,
            'pageNo': form.pageNo.data or 1,
            'pageSize': form.pageSize.data or 10,
            'name': form.name.data or '',
            'code': form.code.data or '',
            'type':form.type.data or True,
            'parent_id':form.parent_id.data or '',
        }
        obj=Department()
        result = obj.query_conditions(kwargs)
        objs.fill({
            'total': result['total'],
            'departments': result['data'],
            'pageNo':kwargs['pageNo'],
            'pageSize': kwargs['pageSize'],
            'success':True
            })
    return json.dumps(objs,default=lambda o:o.__dict__)
