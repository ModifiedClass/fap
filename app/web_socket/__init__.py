# -*- coding:utf-8 -*-

from flask import Blueprint
from app.block.analysis import sock


def create_blueprint_socket():
    # 创建蓝图对象
    bp_sock = Blueprint('sock', __name__)
    
    sock.sockets.register(bp_sock, url_prefix='/analysis')

    return bp_sock