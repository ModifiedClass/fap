# -*- coding:utf-8 -*-

from app.libs.redprint import Redprint
from app.libs.verification_code import ImageCode


api = Redprint('verificationCode')


@api.route('/verification_code', methods=['GET'])
def verification_code():
    return ImageCode().get_img_code()


"""
前端显示
<img src="/api/v1/imgCode" onclick="this.src='/api/v1/verification_code?'+ Math.random()">

后端接收
captcha = request.form.get('captcha').lower()
if captcha==session['imageCode'].lower():
    pass
else：
    return jsonify({'code':-1,'msg':'图片验证码错误'})
"""
