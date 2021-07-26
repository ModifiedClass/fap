# -*- coding:utf-8 -*-
# 文件上传处理
import os
import random
from datetime import datetime
from werkzeug.utils import secure_filename
from flask import jsonify, send_from_directory

# 当前位置绝对路径
# os.getcwd() 或
# os.path.abspath(os.path.dirname(__file__))
# 上上级目录
# os.path.abspath(os.path.join(os.getcwd(), "../.."))
# base_dir = os.path.abspath(os.path.dirname(__file__), "..")
base_dir = os.path.join(os.path.abspath('.'),'app')
upload_path = os.path.join(base_dir, 'static\\files')

def upload(f):
    # 获取安全文件名 避免出现后缀bug
    filename = secure_filename(f.filename)
    randow_num = random.randint(1000, 9999)
    # 新文件名=日期+随机数+文件名后缀
    nfilename = datetime.now().strftime('%Y%m%d%H%M%S') + str(randow_num) + '.' + filename.rsplit('.', 1)[1]
    if not os.path.exists(upload_path):
        os.makedirs(upload_path, 775)
    file_path = os.path.join(upload_path,nfilename)
    f.save(file_path)
    url = '/static/files/' + nfilename
    return url,nfilename


def url_list(filename):
    data = {'filename': filename}
    return data


def files():
    if not os.path.exists(upload_path):
        os.makedirs(upload_path)
    file_list = os.listdir(upload_path)
    return jsonify(list(map(url_list, file_list)))


def download(filename):
    if os.path.isfile(os.path.join(upload_path, filename)):
        # as_attachement=True 这只后浏览器不会直接打开
        return send_from_directory(upload_path, filename, as_attachement=True)


def delete(filename):
    if os.path.isfile(os.path.join(upload_path, filename)):
        os.remove(os.path.join(upload_path, filename))
        return True
    else:
        return False

#上传图片
def save_image(f):
    # 获取安全文件名 避免出现后缀bug
    filename = secure_filename(f.filename)
    randow_num = random.randint(1000, 9999)
    # 新文件名=日期+随机数+文件名后缀
    filename = datetime.now().strftime('%Y%m%d%H%M%S') + str(randow_num) + '.' + filename.rsplit('.', 1)[1]
    full_filename = "%s\\%s" % (os.path.join(base_dir, 'static\\avatar'), filename)
    #linux服务器full_filename = "%s/%s" % (os.path.join(base_dir, 'static\\avatar'), filename)
    #url="%s/%s" % ('media/img', filename)
    url='http://127.0.0.1:8000/static/avatar/'+filename

    if not os.path.exists(upload_path):
        os.makedirs(upload_path, 775)
    with open(full_filename, 'wb+') as destination:
        for chunk in files.chunks():
            destination.write(chunk)
    return filename, full_filename,url