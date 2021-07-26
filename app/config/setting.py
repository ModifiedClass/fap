import os

# app目录
# BASE_DIR = os.path.abspath(os.path.dirname(__file__), os.path.pardir)
BASE_DIR = os.path.join(os.path.abspath("."),'app')
# 分页 每页条目数
# 前端使用方法
# from flask import current_app
# current_app.config['PER_PAGE']
PER_PAGE = 15

# jsonify 中文乱码问题
JSONIFY_MIMETYPE = "application/json;charset=utf-8" #指定浏览器渲染的文件类型，和解码格式；
