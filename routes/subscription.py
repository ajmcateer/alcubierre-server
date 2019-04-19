import functools
import hashlib
import datetime
from os import urandom
from return_status import to_error_json
from models.device import Device
from models.channel import Channel
from models.subscription import Subscription
from models.channel import Channel
from sqlalchemy import text

from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for, jsonify
)

from shared import db
bp = Blueprint('subscription', __name__, url_prefix='/subscription')


@bp.route('/subscribe', methods=['POST'])
def register():
    uuid = request.form.get('uuid')
    channel_key = request.form.get('channel_key')

    if not uuid:
        return to_error_json("uuid is required")
    elif not channel_key:
        return to_error_json("channel_key is required")

    sub = Subscription.query.filter_by(uuid=uuid).filter_by(channel_key=channel_key).first()

    if sub is None:
        channel_name = Channel.query.with_entities(Channel.name).filter_by(listen_key=channel_key).first()
        subscription = Subscription(uuid=uuid, channel_key=channel_key, channel_name=channel_name[0])
        db.session.add(subscription)
        db.session.commit()
        return jsonify(subscription.dict())
    else:
        return to_error_json("Subscription already exists")
