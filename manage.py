# -*- coding:utf-8 -*-

from app import create_app
from flask import send_file
import os
# flask-script
# from flask_script import Manager
# flask-script
# flask-migrate
# from flask_migrate import Migrate,MigrateCommand
# flask-migrate


app = create_app()
# flask-script: manager = Manager(app)
# flask-migrate:migrate = Migrate(app,db)
# manage.add_command('db',MigrateCommand)


@app.route('/favicon.ico')
def favicon():
    file_path = os.path.join(os.path.abspath("."),'favicon.ico')
    return send_file(file_path)


if __name__ == '__main__':
    app.run(debug=True)
    # flask-script: manager.run()
    # websocket
    #from geventwebsocket.handler import WebSocketHandler
    #from gevent.pywsgi import WSGIServer
    #app.debug = True
    #http_serv = WSGIServer(('0.0.0.0',5000),app,handler_class=WebSocketHandler)
    #http_serv.serve_forever()
    # 注释app.run ws与http都可以使用
    # websocket


# flask-script:入口文件改为manage.py 使用python manage.py runserver运行程序
# flask-migrate:python manage.py db init
# flask-migrate:python manage.py db migrate
# flask-migrate:python manage.py db upgrade