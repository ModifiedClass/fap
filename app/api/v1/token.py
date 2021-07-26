# -*- coding:utf-8 -*-

from flask import current_app, jsonify,g
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer, SignatureExpired, \
    BadSignature

from app.libs.redprint import Redprint
from app.block.permission.validator import ClientForm, TokenForm, UidForm
from app.libs.enums import ClientTypeEnum
from app.block.permission.model import User
from app.libs.error_code import AuthFailed



api = Redprint('token')


# 获取token 就是登录
@api.route('', methods=['POST'])
def get_token():
    form = ClientForm().validate_for_api()
    promise = {
        ClientTypeEnum.USER_EMAIL: User.verify,
        ClientTypeEnum.USER_MOBILE: User.verify,
        ClientTypeEnum.USER_NICKNAME: User.verify
    }
    # identity就是User.verify返回的字典uid
    identity = promise[ClientTypeEnum(form.type.data)](
        ClientTypeEnum(form.type.data),
        form.account.data,
        form.secret.data
    )
    # Token
    expiration = current_app.config['TOKEN_EXPIRATION']
    token = generate_auth_token(
        identity['uid'],
        form.type.data,
        identity['rules'],
        expiration
    )
    t = {
        'token': token.decode('ascii'),
        'uid': identity['uid']
    }
    return jsonify(t), 201


# 验证token是否合法有效
@api.route('/secret', methods=['POST'])
def get_token_info():
    """获取令牌信息"""
    form = TokenForm().validate_for_api()
    s = Serializer(current_app.config['SECRET_KEY'])
    try:
        data = s.loads(form.token.data, return_header=True)
    except SignatureExpired:
        raise AuthFailed(msg='token is expired', error_code=1003)
    except BadSignature:
        raise AuthFailed(msg='token is invalid', error_code=1002)
    
    print('tokeninfo:',data)
    r = {
        'rules': data[0]['rules'],
        'create_at': data[1]['iat'], #生成时间
        'expire_in': data[1]['exp'], #过期时间
        'uid': data[0]['uid']
    }
    return jsonify(r)


def generate_auth_token(uid, ac_type, rules=None, expiration=7200):
    """生成令牌"""
    s = Serializer(current_app.config['SECRET_KEY'], expires_in=expiration)
    return s.dumps({
        'uid': uid,
        'type': ac_type.value,
        'rules': rules
    })


@api.route('/userinfo', methods=['GET'])
def get_user_info():
    #uid=g.user.id
    form = UidForm().validate_for_api()
    user=User.query.filter_by(id=form.uid.data).first_or_404()
    current_rules = get_user_rules_by_user(user)
    userauth = {
        "avatar": user.avatar,
        "email": user.email,
        "gender": user.gender,
        "id": user.id,
        "id_number": user.id_number,
        "last_login_time": user.last_login_time,
        "mobile": user.mobile,
        "nickname": user.nickname,
        "realname": user.realname,
        "current_rules": current_rules,
    }
    #return jsonify({'userauth': userauth})
    return jsonify(userauth)


@api.route('/usermenu', methods=['GET'])
def get_user_menu():
    from app.block.permission.model import Menu
    from app.libs.menu_builder import FlatToNested
    form = UidForm().validate_for_api()
    user=User.query.filter_by(id=form.uid.data).first_or_404()
    all_menus = Menu().query_conditions(kwargs={})
    current_rules = get_user_rules_by_user(user)
    leaves_menus = get_dict_leaves_menus_by_rules(current_rules)
    current_flat_menus = build_user_dict_menus(all_menus['data'],leaves_menus)
    current_trees_menus = FlatToNested(current_flat_menus)
    # return jsonify({'usermenu': current_trees_menus['sub'][0]['sub']})
    return jsonify(current_trees_menus['children'][0]['children'])



def get_user_rules_by_user(user):
    # 获取该用户的所有组
    groups=user.groups.all()
    # 用户组包含的权限
    urs=[]
    for g in groups:
        rs=g.rules.all()
        for r in rs:
            if r not in urs:
                urs.append(r)
    return urs


def get_user_rules_by_uid(uid):
    user=User.query.filter_by(id=uid).first_or_404()
    # 获取该用户的所有组
    groups=user.groups.all()
    # 用户组包含的权限
    urs=[]
    for g in groups:
        rs=g.rules.all()
        for r in rs:
            if r not in urs:
                urs.append(r)
    return urs

def get_leaves_menus_by_rules(rules):
    from app.block.permission.model import Menu
    # 当前用户叶子菜单
    menus=[]
    for rule in rules:
        if rule.menu_id:
            m=Menu.query.filter_by(id=rule.menu_id).first_or_404()
            if m not in menus:
                menus.append(m)
    new_menus=[]
    for m in menus:
        # 构造当前菜单下操作权限
        current_rules=[]
        for rule in rules:
            if rule.menu_id == m.id:
                current_rules.append(rule)
        m.current_rules=current_rules
        new_menus.append(m)
    #obj = sorted(new_menus, key=lambda k: k['sort'], reverse=False)
    return new_menus


def build_user_menus(complate_menus,leaves_menus):
    import copy
    temp = copy.deepcopy(leaves_menus)
    # 当前用户菜单长度
    current_temp_len=0
    # 循环后用户菜单长度
    next_temp_len=0
    while 1:
        # 当前用户菜单长度重新计数
        current_temp_len = len(temp)
        for t in temp:
            for cm in complate_menus:
                # 找到当前用户菜单的父菜单，加入当前用户菜单列表
                if cm.id == t.parent_id and cm not in temp:
                    temp.append(cm)
                    # 循环后用户菜单长度变化
                    next_temp_len = len(temp)
        # 用户菜单长度不变化时，构造完毕，退出循环
        if current_temp_len == next_temp_len:
            break
    return temp


def get_dict_leaves_menus_by_rules(rules):
    from app.block.permission.model import Menu
    # 当前用户叶子菜单
    menus=[]
    for rule in rules:
        if rule.menu_id:
            m=Menu.query.filter_by(id=rule.menu_id).first_or_404()
            if m not in menus:
                menus.append(m)
    new_menus=[]
    for m in menus:
        # 构造当前菜单下操作权限
        current_rules=[]
        for rule in rules:
            if rule.menu_id == m.id:
                current_rules.append(rule)
        m.current_rules=current_rules
        new_menus.append({
            "component": m.component,
            "hide_children": m.hide_children,
            "hide_self": m.hide_self,
            "icon": m.icon,
            "id": m.id,
            "name": m.name,
            "parent_id": m.parent_id,
            "path": m.path,
            "sort": m.sort,
            "current_rules":m.current_rules
        })
    #obj = sorted(new_menus, key=lambda k: k['sort'], reverse=False)
    return new_menus


def build_user_dict_menus(complate_menus,leaves_menus):
    import copy
    temp = copy.deepcopy(leaves_menus)
    # 当前用户菜单长度
    current_temp_len=0
    # 循环后用户菜单长度
    next_temp_len=0
    while 1:
        # 当前用户菜单长度重新计数
        current_temp_len = len(temp)
        for t in temp:
            for cm in complate_menus:
                # 找到当前用户菜单的父菜单，加入当前用户菜单列表
                if cm.id == t['parent_id'] and cm not in temp:
                    temp.append(cm)
                    # 循环后用户菜单长度变化
                    next_temp_len = len(temp)
        # 用户菜单长度不变化时，构造完毕，退出循环
        if current_temp_len == next_temp_len:
            break
    return temp


@api.route('/complatemenus', methods=['GET'])
def treemenus():
    from app.block.permission.model import Menu
    from app.libs.menu_builder import FlatToNested
    form = UidForm().validate_for_api()
    user=User.query.filter_by(id=form.uid.data).first_or_404()
    all_menus = Menu().query_conditions(kwargs={})
    current_rules = get_user_rules_by_user(user)
    leaves_menus = get_dict_leaves_menus_by_rules(current_rules)
    current_flat_menus = build_user_dict_menus(all_menus['data'],leaves_menus)
    current_trees_menus = FlatToNested(current_flat_menus)
    usermenu = {
        "current_flat_menus": current_flat_menus,
        "current_trees_menus": current_trees_menus
    }
    return jsonify({'usermenu': usermenu})

