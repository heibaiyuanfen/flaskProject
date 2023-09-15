from flask import Blueprint
from flask import render_template, session
from flask_socketio import leave_room, join_room, emit

bp = Blueprint("chat", __name__, url_prefix ="/chat")
# 聊天室列表
chat_rooms = {}
# 聊天页面
@bp.route('/index')
def chat():
    # return render_template('chat.html')
    return "chathtml"
# 处理用户加入聊天室
@bp.route("/join")
def on_join(data):
    username = data['username']
    room = data['room']

    join_room(room)
    session['room'] = room

    if room not in chat_rooms:
        chat_rooms[room] = []

    chat_rooms[room].bpend(username)

    emit('update_users', {'users': chat_rooms[room]}, room=room)
    emit('message', {'message': f'{username} 加入了聊天室 {room}'}, room=room)


# 处理用户离开聊天室
@bp.route('/leave')
def on_leave(data):
    username = data['username']
    room = session['room']

    leave_room(room)

    if room in chat_rooms:
        chat_rooms[room].remove(username)

    emit('update_users', {'users': chat_rooms[room]}, room=room)
    emit('message', {'message': f'{username} 离开了聊天室 {room}'}, room=room)


# 处理用户发送消息
@bp.route('/send_message')
def send_message(data):
    message = data['message']
    room = session['room']

    emit('message', {'message': f'{data["username"]}: {message}'}, room=room)
