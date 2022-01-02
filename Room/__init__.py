import os

from flask_pymongo import PyMongo
from flask import Flask, render_template, request
from flask_login import LoginManager
from flask_login import login_user, login_required, logout_user, current_user
from flask_socketio import SocketIO, join_room, leave_room
from flask import Flask
from flask_mail import Mail


mail = Mail()
socketio = SocketIO()
login_manager = LoginManager()
mongo1 = PyMongo()

def init_app():
    app1 = Flask(__name__,instance_relative_config=False)
    app1.config.from_pyfile('config.py')
    socketio.init_app(app1)
    mongo1.init_app(app1)
    login_manager.init_app(app1)
    mail.init_app(app1)
    db_operations = mongo1.db.users

    @app1.route("/")
    def hello():
        messages = request.args.get('message')
        if messages is not None:
            return render_template("index.html", message = messages)
        else:
            return render_template("index.html")

    @app1.route("/chat")
    @login_required
    def chat():
        name = current_user.firstname
        return render_template("chat.html", name = name, room = 'room' )

    @socketio.on('join_room')
    def handle_my_custom_event(data):
        print('received json: ' + str(data))
        join_room(data['room'])
        socketio.emit("join_room_announcement", data )

    @socketio.on('send_message')
    def handle_send_message_event(data):
        print("received message" + str(data))
        socketio.emit('receive_message', data)

    @socketio.on('leave_room')
    def handle_my_stop_event(data):
        print('received data leave: ' + str(data))
        leave_room(data['room'])
        socketio.emit("leave_room_announcement", data )


    from Room.auth.view import auth_obj
    
    app1.register_blueprint(auth_obj)


        
    return app1