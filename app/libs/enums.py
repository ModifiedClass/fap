# -*- coding:utf-8 -*-

from enum import Enum


class ClientTypeEnum(Enum):
    # 用户邮箱
    USER_EMAIL = 100
    # 手机号登录
    USER_MOBILE = 101
    # 昵称登录
    USER_NICKNAME = 102

    # 小程序登录
    USER_MINA = 200
    # 微信登录
    USER_WX = 201
