from flask import Flask
from Room import init_app
from Room import socketio


app = init_app()

if __name__ == "__main__":
    socketio.run(app, debug = True)