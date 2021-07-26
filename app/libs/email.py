# -*- coding:utf-8 -*-

# pipenv install flask-mail
from flask_mail import Mail
from flask_mail import Message
from flask import current_app, render_template
from threading import Thread

mail = Mail()


def send_async_email(app, msg):
    with app.app_context():
        try:
            mail.send(msg)
        except Exception as e:
            raise e


def send_main(to, subject, template, **kwargs):
    # msg=Message('邮件标题',sender='配置文件中的MAIL_USERNAME',body='正文',recipients=['@qq.com'])
    msg = Message(subject, sender=current_app.config['MAIL_USERNAME'], recipients=[to])
    msg.html = render_template(template, **kwargs)
    app = current_app.__get_current_object()
    thr = Thread(target=send_async_email, args=[app, msg])
    thr.start()

# 前端使用 send_mail(form.email.data,'重置密码', 'email/reset_password.html',user=user,token=user.generate_token)
