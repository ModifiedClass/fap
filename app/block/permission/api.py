# -*- coding:utf-8 -*-

from flask import g
from app.libs.redprint import Redprint
from app.libs.token_auth import auth
from app.models.mysql.base import db
from app.block.permission.validator import \
    RuleInsertForm, RuleUpdateForm, RuleGetForm, RuleSearchForm, RuleDeleteForm, IdsForm,\
    MenuInsertForm, MenuUpdateForm, MenuGetForm, MenuSearchForm, MenuDeleteForm, \
    GroupInsertForm, GroupUpdateForm,GroupGetForm, GroupSearchForm, GroupDeleteForm, \
    UserInsertForm, UserUpdateForm,UserGetForm, UserSearchForm, UserDeleteForm, \
    ClientForm,UserResetPasswordForm
from app.block.permission.view_model import GroupCollection, RuleCollection, MenuCollection, UserCollection
from app.block.permission.view_model_antd import MenuAntdCollection,MenuAntdPage
from .services import create_client as scc, \
    menu_edit as smenu_edit,menu_delete as smenu_delete, menu_get as smenu_get,menu_query as smenu_query, \
    rule_edit as srule_edit,rule_delete as srule_delete, rule_get as srule_get,rule_query as srule_query, \
    group_edit as sgroup_edit,group_delete as sgroup_delete, \
    group_get as sgroup_get,group_query as sgroup_query,group_rules as sgroup_rules, \
    user_edit as suser_edit,user_delete as suser_delete, user_reset_password as suser_reset_password,\
    user_get as suser_get,user_query as suser_query, user_groups as suser_groups,user_departments as suser_departments ,\
    user_export as suser_export


# auth
auth_api = Redprint('auth')


@auth_api.route('/register', methods=['POST'])
def create_client():
    # 注册 登录
    # 参数 校验 接收参数
    # WTForms 验证表单
    return scc(ClientForm().validate_for_api())


# menu
menu_api = Redprint('menu')

@menu_api.route('', methods=['POST'])
@auth.login_required
def menu_post():
    return smenu_edit(MenuInsertForm().validate_for_api())


@menu_api.route('', methods=['DELETE'])
@auth.login_required
def menu_delete():
    return smenu_delete(MenuDeleteForm().validate_for_api())


@menu_api.route('', methods=['PUT'])
@auth.login_required
def menu_put():
    return smenu_edit(MenuUpdateForm().validate_for_api())


@menu_api.route('', methods=['GET'])
@auth.login_required
def menu_get():
    return smenu_get(MenuGetForm().validate_for_api())


@menu_api.route('/antd', methods=['GET'])
@auth.login_required
def menu_antd_get():
    res = smenu_get(MenuGetForm().validate_for_api(),MenuAntdPage(),'antd')
    return res


@menu_api.route('/collection', methods=['GET'])
@auth.login_required
def menu_query():
    return smenu_query(MenuSearchForm(),MenuCollection())


@menu_api.route('/collection/antd', methods=['GET'])
@auth.login_required
def menu_antd_query():
    return smenu_query(MenuSearchForm(),MenuAntdCollection(),'antd')



# rule
rule_api = Redprint('rule')

@rule_api.route('', methods=['POST'])
@auth.login_required
def rule_post():
    return srule_edit(RuleInsertForm().validate_for_api())


@rule_api.route('', methods=['DELETE'])
@auth.login_required
def rule_delete():
    return srule_delete(RuleDeleteForm().validate_for_api())


@rule_api.route('', methods=['PUT'])
@auth.login_required
def rule_put():
    return srule_edit(RuleUpdateForm().validate_for_api())



@rule_api.route('', methods=['GET'])
@auth.login_required
def rule_get():
    return srule_get(RuleGetForm().validate_for_api())


@rule_api.route('/collection', methods=['GET'])
@auth.login_required
def rule_query():
    return srule_query(RuleSearchForm(),RuleCollection())



# group
group_api = Redprint('group')

@group_api.route('', methods=['POST'])
@auth.login_required
def group_post():
    return sgroup_edit(GroupInsertForm().validate_for_api())


@group_api.route('', methods=['DELETE'])
@auth.login_required
def group_delete():
    return sgroup_delete(GroupDeleteForm().validate_for_api())


@group_api.route('', methods=['PUT'])
@auth.login_required
def group_put():
    return sgroup_edit(GroupUpdateForm().validate_for_api())



@group_api.route('', methods=['GET'])
@auth.login_required
def group_get():
    return sgroup_get(GroupGetForm().validate_for_api())


@group_api.route('/collection', methods=['GET'])
@auth.login_required
def group_query():
    return sgroup_query(GroupSearchForm(),GroupCollection())



@group_api.route('/rules', methods=['PUT'])
@auth.login_required
def group_rules():
    return sgroup_rules(IdsForm().validate_for_api())



user_api = Redprint('user')

""" 
@user_api.route('', methods=['GET'])
# libs/token_auth中的验证方法
@auth.login_required
def get_user():
    # 验证token是否合法 是否过期
    print('user:')
    uid = g.user.id
    # g线程隔离 不同用户访问不会冲突
    user = User.query.filter_by(id=uid).first_or_404()
    # dict
    # view_model
    # 视图层 个性化的视图模型
    return jsonify(user)
"""


@user_api.route('', methods=['POST'])
@auth.login_required
def user_post():
    return suser_edit(UserInsertForm().validate_for_api())


@user_api.route('', methods=['DELETE'])
@auth.login_required
def user_delete():
    return suser_delete(UserDeleteForm().validate_for_api())


@user_api.route('', methods=['PUT'])
@auth.login_required
def user_put():
    return suser_edit(UserUpdateForm().validate_for_api())


@user_api.route('', methods=['GET'])
@auth.login_required
def user_get():
    return suser_get(UserGetForm().validate_for_api())


@user_api.route('/collection', methods=['GET'])
@auth.login_required
def user_query():
    return suser_query(UserSearchForm(),UserCollection())


@user_api.route('/resetpassword', methods=['PUT'])
@auth.login_required
def user_reset_password():
    return suser_reset_password(UserResetPasswordForm().validate_for_api())


@user_api.route('/groups', methods=['PUT'])
@auth.login_required
def user_groups():
    return suser_groups(IdsForm().validate_for_api())


@user_api.route('/departments', methods=['PUT'])
@auth.login_required
def user_departments():
    return suser_departments(IdsForm().validate_for_api())



@user_api.route('/avatar', methods=['PUT'])
@auth.login_required
def user_avatar():
    from flask import request,json
    from app.libs.upload import save_image
    ret={'status':0,'msg':None,'data':None}
    f = request.FILES['avatar']
    try:
        filename,full_filename,url=save_image(f)
        ret['status']=1
        ret['data']=[filename,full_filename,url]
        ret['msg']="操作成功!"
        return json.dumps(ret,ensure_ascii=False)
    except Exception as e:
        return json.dumps(ret,ensure_ascii=False)


@user_api.route('/export', methods=['GET'])
@auth.login_required
def user_export():
    return suser_export(UserSearchForm().validate_for_api())


"""
# from flask import views
# from app.libs.cache import cache
CBV
class Group(views.MethodView):
    methods = ['get', 'post', 'head', 'options','delete', 'put', 'trace', 'patch']#可以在类中指定允许的请求方式，不指定会根据定义的函数进行选择
    # decorators = []#对类中的函数都加上装饰器，列表中可以放多个装饰器函数名，以此执行

    # @cache.cached(timeout=60*2)
    # @auth.login_required
    def get(self):
        return 'index get method'

api.add_url_rule('/group', view_func=Group.as_view(name='group'))
""" 
