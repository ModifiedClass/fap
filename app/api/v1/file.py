# -*- coding:utf-8 -*-
import os
from flask import request

from app.libs.redprint import Redprint
from app.libs.error_code import DeleteSuccess, ServerError
from app.libs.upload import upload, download, files, delete


api = Redprint('file')


@api.route('/', methods=['POST'])
def upload_file():
    if request.method == 'POST' and 'files' in request.files:
        f = request.files['files']
        # f=request.files.get('file')
        return upload(f)
    else:
        return ServerError()


@api.route('/', methods=['GET'])
def file_list():
    return files()


@api.route('/download', methods=['GET'])
def download_file():
    return download(request.args.get("filename"))


@api.route('/', methods=['DELETE'])
def delete_file():
    if delete(request.args.get("filename")):
        return DeleteSuccess()
    else:
        return ServerError()
