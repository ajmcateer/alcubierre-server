from flask import Blueprint
from models.device import Device

bp = Blueprint('websocket', __name__, url_prefix='/websocket')
ws_dict = {}


@bp.route('/echo')
def echo_socket(ws):
    message = ws.receive()
    if message == "ping" and not ws.closed:
        ws.send("pong")
    else:
        uuid = message
        device = Device.query.filter(Device.uuid == uuid).first()

        if not device:
            ws.send("Not Valid Device")
        elif uuid not in ws_dict:
            ws_dict[uuid] = ws
            ws.send("Connection Successful")


