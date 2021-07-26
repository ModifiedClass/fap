# -*- coding:utf-8 -*-
from flask import json,jsonify
from app.block.permission.validator import UserEmailForm, UserMobileForm, UserNickNameForm
from app.libs.enums import ClientTypeEnum
from app.block.permission.model import Rule, Menu, Group, User
from app.libs.error_code import DeleteSuccess,Success


def create_client(form):
    promise = {
        ClientTypeEnum.USER_EMAIL: __register_user_by_email,
        ClientTypeEnum.USER_MOBILE: __register_user_by_mobile,
        ClientTypeEnum.USER_NICKNAME: __register_user_by_username
    }

    # promise[form.type.data] = __register_user_by_email 加() 代表调用这个函数
    promise[form.type.data]()
    # 我们可以预知已知的异常 APIException
    # 我们没法预知未知的异常

    # AOP 出口处理未知异常
    # {code = 201,msg = 'ok',error_code = 0}
    return Success()


def __register_user_by_email():
    # validate_for_api()已实现data=data可以获取视图模型数据
    form = UserEmailForm().validate_for_api()
    User.register_by_email(form.account.data, form.secret.data)


def __register_user_by_mobile():
    form = UserMobileForm().validate_for_api()
    User.register_by_mobile(form.account.data, form.secret.data)


def __register_user_by_username():
    form = UserNickNameForm().validate_for_api()
    User.register_by_username(form.account.data, form.secret.data)



# menu

def menu_edit(form):
    obj = {
        'id':form.id.data,
        'name':form.name.data,
        'remark':form.remark.data,
        'hide_children':form.hide_children.data,
        'hide_self':form.hide_self.data,
        'icon':form.icon.data,
        'path':form.path.data,
        'component':form.component.data,
        'sort':form.sort.data,
        'parent_id':form.parent_id.data
    }
    if form.id.data != None and form.id.data != '':
        Menu.update(obj)
    else:
        Menu.create(obj)
    return Success()


def menu_delete(form):
    Menu.query.filter_by(id=form.id.data).first_or_404().delete()
    return DeleteSuccess()


def menu_get(form,objs={},sign=''):
    if sign == 'antd':
        obj = Menu.query.filter_by(id=form.id.data).first_or_404()
        obj.message='ok'
        obj.success=True
        objs.fillantd(obj)
        return json.dumps(objs,default=lambda o:o.__dict__,ensure_ascii=False, encoding="utf-8")
    else:
        return jsonify(Menu.query.filter_by(id=form.id.data).first_or_404())


def menu_query(form,objs,sign=''):
    kwargs = {
        'ispage':form.ispage.data,
        'pageNo': form.pageNo.data or 1,
        'pageSize': form.pageSize.data or 10,
        'name': form.name.data or '',
        'remark': form.remark.data or '',
        'hide_children':form.hide_children.data or '',
        'hide_self':form.hide_self.data or '',
        'path':form.path.data or '',
        'sort':form.sort.data or '',
        'parent_id':form.parent_id.data or ''
    }
    obj=Menu()
    result = obj.query_conditions(kwargs)
    if sign == 'antd':
        objs.fillantd({
            'total': result['total'],
            'menus': result['data'],
            'success': True,
            'pageSize':kwargs['pageSize'],
            'pageNo':kwargs['pageNo']
        })
    else:
        objs.fill({
            'total': result['total'],
            'menus': result['data'],
            'success': True,
            'pageSize':kwargs['pageSize'],
            'pageNo':kwargs['pageNo']
        })
    return json.dumps(objs,default=lambda o:o.__dict__,ensure_ascii=False, encoding="utf-8")


# rule

def rule_edit(form):
    obj={
        'id':form.id.data,
        'name':form.name.data,
        'remark':form.remark.data,
        'api':form.api.data,
        'method':form.method.data,
        'func':form.func.data,
        'menu_id':form.menu_id.data
    }
    if form.id.data != None and form.id.data != '':
        Rule.update(obj)
    else:
        Rule.create(obj)
    return Success()


def rule_delete(form):
    Rule.query.filter_by(id=form.id.data).first_or_404().delete()
    return DeleteSuccess()


def rule_get(form):
    return jsonify(Rule.query.filter_by(id=form.id.data).first_or_404())


def rule_query(form,objs):
    kwargs = {
        'ispage':form.ispage.data,
        'pageNo': form.pageNo.data or 1,
        'pageSize': form.pageSize.data or 10,
        'name': form.name.data or '',
        'api': form.api.data or '',
        'method': form.method.data or '',
        'func': form.func.data or '',
        'menu_id': form.menu_id.data or '',
        'remark': form.remark.data or ''
    }
    obj=Rule()
    result = obj.query_conditions(kwargs)
    objs.fill({
        'total': result['total'],
        'rules': result['data'],
        'success': True,
        'pageSize':kwargs['pageSize'],
        'pageNo':kwargs['pageNo']
    })
    return json.dumps(objs,default=lambda o:o.__dict__,ensure_ascii=False, encoding="utf-8")



# group

def group_edit(form):
    obj = {'id':form.id.data,'name':form.name.data,'remark':form.remark.data}
    if form.id.data != None and form.id.data != '':
        Group.update(obj)
    else:
        Group.create(obj)
    return Success()


def group_delete(form):
    Group.query.filter_by(id=form.id.data).first_or_404().delete()
    return DeleteSuccess()


def group_get(form):
    return jsonify(Group.query.filter_by(id=form.id.data).first_or_404())


def group_query(form,objs):
    kwargs = {
        'ispage':form.ispage.data,
        'pageNo': form.pageNo.data or 1,
        'pageSize': form.pageSize.data or 10,
        'name': form.name.data or ''
    }
    obj=Group()
    result = obj.query_conditions(kwargs)
    objs.fill({
        'total': result['total'],
        'groups': result['data'],
        'success': True,
        'pageSize':kwargs['pageSize'],
        'pageNo':kwargs['pageNo']
    })
    return json.dumps(objs,default=lambda o:o.__dict__,ensure_ascii=False, encoding="utf-8")


def group_rules(form):
    Group.update({'id':form.id.data,'ruleids':[ int(x) for x in form.ids.data.split(',') ]})
    return Success()


def user_edit(form):
    obj={
        'id':form.id.data,
        'nickname':form.nickname.data,
        'remark':form.remark.data,
        'email':form.email.data,
        'mobile':form.mobile.data,
        'nickname':form.nickname.data,
        'password':form.password.data,
        'last_login_time':form.last_login_time.data,
        'realname':form.realname.data,
        'gender':form.gender.data,
        'id_number':form.id_number.data,
        'avatar':form.avatar.data,
        'groupids':form.groupids.data,
        'departmentids':form.departmentids.data,
    }
    if form.id.data != None and form.id.data != '':
        User.update(obj)
    else:
        User.create(obj)
    return Success()


def user_delete(form):
    User.query.filter_by(id=form.id.data).first_or_404().delete()
    return DeleteSuccess()


def user_get(form):
    return jsonify(User.query.filter_by(id=form.id.data).first_or_404())


def user_query(form,objs):
    kwargs = {
        'ispage':form.ispage.data,
        'pageNo': form.pageNo.data or 1,
        'pageSize': form.pageSize.data or 10,
        'nickname': form.nickname.data or '',
        'email':form.email.data or '',
        'mobile':form.mobile.data or '',
        'nickname':form.nickname.data or '',
        'realname':form.realname.data or '',
        'gender':form.gender.data or '',
        'id_number':form.id_number.data or '',
        'create_time_start':form.create_time_start.data or '',
        'create_time_end':form.create_time_end.data or ''
    }
    obj=User()
    result = obj.query_conditions(kwargs)
    objs.fill({
        'total': result['total'],
        'users': result['data'],
        'success': True,
        'pageSize':kwargs['pageSize'],
        'pageNo':kwargs['pageNo']
        })
    return json.dumps(objs,default=lambda o:o.__dict__,ensure_ascii=False, encoding="utf-8")


def user_reset_password(form):
    User.update({'id':form.id.data,'password':form.password.data})
    return Success()


def user_groups(form):
    print('ids:',form.ids.data)
    User.update({'id':form.id.data,'groupids':list(map(int, form.ids.data.split(',')))})
    return Success()


def user_departments(form):
    User.update({'id':form.id.data,'departmentids':[ int(x) for x in form.ids.data.split(',') ]})
    return Success()


def user_export(form):
    from flask import make_response
    from urllib.parse import quote
    import xlsxwriter
    import datetime
    from io import BytesIO
    from app.libs.datetime_helper import strptime_to_str

    kwargs = {
        'create_time_start':form.create_time_start.data or '',
        'create_time_end':form.create_time_end.data or ''
    }
    obj=User().query_conditions(kwargs)
    data = obj['data']
    # 创建IO对象
    output = BytesIO()
    # 写excel
    workbook = xlsxwriter.Workbook(output)  # 先创建一个book，直接写到io中
    sheet = workbook.add_worksheet() # 默认'sheet1'
    fileds = ['id', 'email', 'mobile', 'nickname', 'last_login_time', #表头
    'realname', 'gender', 'id_number', 'avatar', 'remark']

    # 写入数据到第一行
    sheet.write_row('A1', fileds)
    # 遍历有多少行数据
    for i in range(len(data)):
        # 遍历有多少列数据
        for x in range(len(fileds)):
            key = [key for key in data[i].keys()]
            if key[x] == 'last_login_time':
                sheet.write(i + 1, x, strptime_to_str(data[i][key[x]]))
            elif key[x] == 'gender':
                if data[i][key[x]] == 1:
                    sheet.write(i + 1, x, '男')
                elif data[i][key[x]] == 2:
                    sheet.write(i + 1, x, '女')
                else:
                    sheet.write(i + 1, x, '其他')
            else:
                sheet.write(i + 1, x, data[i][key[x]])

    workbook.close()  # 需要关闭
    output.seek(0)  # 找到流的起始位置

    # 设置HTTPResponse的类型
    response = make_response(output.getvalue())
    basename = quote('用户数据_{}.xlsx'.format(datetime.datetime.now().strftime("%Y%m%d%H%M%S")).encode('utf-8'))

    # 转码，支持中文名称
    response.headers["Content-Disposition"] = "attachment; filename*=UTF-8''{utf_filename}".format(
        utf_filename=basename
    )
    response.headers['Content-Type'] = 'application/x-xlsx'

    return response