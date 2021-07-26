# pipenv install gevent-websocket
# from flask import Blueprint,request
# from geventwebsocket.handler import WebSocketHandler
# from gevent.pywsgi import WSGIServer
""" from geventwebsocket.websocket import WebSocket
import json

user_socket_dict={}
def create_websocket(app):
    # 创建蓝图对象
    wsb = Blueprint('wsb', __name__)
    @wsb.route('/websocket')
    def ws():
        user_socket = request.environ.get('wsgi.websocket') # type:WebSocket
        user_socket_dict[username] = user_socket
        print(len(user_socket_dict),user_socket_dict)
        while 1:
            try:
                msg = user_socket.receive()
                msg = json.loads(msg)
                to_user = msg.get('to_user')
                content = msg.get('msg')
                usocket = user_socket_dict.get(to_user)
                recv_msg = {
                    'from_user':username,
                    'msg':content
                }
                usocket.send(json.dumps(recv_msg))
            except:
                pass
 """