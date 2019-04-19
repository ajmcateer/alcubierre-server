import functools
import hashlib
import datetime
from os import urandom
from return_status import to_error_json
from models.device import Device
from models.channel import Channel
from models.subscription import Subscription
from models.channel import Channel
from models.messages import Message
from models.message_queue import MessageQueue
from send_message import send_message
from sqlalchemy import text

from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for, jsonify
)

from shared import db
bp = Blueprint('message', __name__, url_prefix='/message')


@bp.route('/send', methods=['POST'])
def dispatch_message():
    channel_name = request.form.get('channel_name')
    admin_key = request.form.get('admin_key')
    title = request.form.get('title')
    body = request.form.get('message')

    if not channel_name:
        return to_error_json("channel_name is required")
    elif not title:
        return to_error_json("title is required")
    elif not body:
        return to_error_json("message is required")

    if Channel.query.filter(Channel.name == channel_name).first() is None:
        return to_error_json("Channel {} does not exist".format(channel_name))

    if Channel.query.filter(Channel.admin_key == admin_key).first() is None:
        return to_error_json("Admin Key does not match any channel")

    message = Message(channel_name=channel_name, title=title, message=body)
    db.session.add(message)
    db.session.commit()
    send_message(message=message, channel_name=channel_name, admin_key=admin_key)
    return jsonify(message.dict())


@bp.route('/', methods=['GET'])
def get_messages():
    uuid = request.args.get('uuid')

    if not uuid:
        return to_error_json("uuid is required")

    stored_messages = MessageQueue.query.filter_by(uuid=uuid).all()

    if stored_messages is None:
        return to_error_json("No messages for your device")

    message_list = []
    for a_message in stored_messages:
        mess = Message.query.filter_by(id=a_message.message_id).first()
        message_list.append(mess.dict())
        print('Test')

    return jsonify(message_list)
