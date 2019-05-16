import os
from shared import db
from config import config
import database
from flask import Flask
from flask_sockets import Sockets
from flask_sqlalchemy import SQLAlchemy
from flask_sockets import Sockets

app = Flask(__name__)
sockets = Sockets(app)

if not app.config['TESTING']:
    project_dir = os.path.dirname(os.path.abspath(__file__))
    database_file = "sqlite:///{}".format(os.path.join(project_dir, "alcu.db"))

    app.config['SQLALCHEMY_DATABASE_URI'] = config['Database']['path']
    sockets = Sockets(app)
    db.init_app(app)
    db.app = app

    try:
        database.init_db()
    except Exception as err:
        print(err)

from routes import channel, register, subscription, messages, websocket
app.register_blueprint(channel.bp)
app.register_blueprint(register.bp)
app.register_blueprint(subscription.bp)
app.register_blueprint(messages.bp)
sockets.register_blueprint(websocket.bp)


@app.route("/", methods=["GET", "POST"])
def home():
    return "I'm Alive"


@app.route('/ret')
def hello():
    for con in websocket.ws_dict:
        if not websocket.ws_dict[con].closed:
            websocket.ws_dict[con].send("Done")
    return 'Hello World!'


if __name__ == "__main__":
    #app.run(debug=True)
    from gevent import pywsgi
    from geventwebsocket.handler import WebSocketHandler

    server = pywsgi.WSGIServer(('', 5000), app, handler_class=WebSocketHandler)
    server.serve_forever()
