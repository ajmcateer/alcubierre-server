import functools
import hashlib
import datetime
from os import urandom
from return_status import to_error_json
from models.device import Device
from sqlalchemy import text

from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for, jsonify
)

from shared import db
bp = Blueprint('register', __name__, url_prefix='/devices')


@bp.route('/register', methods=['POST'])
def register():
    uuid = request.form.get('uuid')
    public_key = request.form.get('public_key')
    name = request.form.get('name')
    message_type = request.form.get('message_type')
    error = None

    if not uuid:
        error = 'uuid is required.'
    elif not name:
        error = 'name is required.'
    elif not message_type:
        error = 'message_type is required.'
    elif Device.query.filter(Device.uuid == uuid).first() is not None:
        error = 'uuid {} is already registered.'.format(uuid)

    if error is None:
        device = Device(uuid=uuid, public_key=public_key, name=name, message_type=message_type)
        db.session.add(device)
        db.session.commit()
        return jsonify(device.dict())

    return 'Registration Failed: {}'.format(error)


@bp.route('/device', methods=['GET'])
def get_device():
    uuid = request.args.get('uuid')
    error = None

    if not uuid:
        error = 'uuid is required.'

    if error is None:
        device = Device.query.filter(Device.uuid == uuid).first()
        if not device:
            return to_error_json("Device {} does not exist".format(uuid))

        return jsonify(device.dict())


@bp.route('/delete', methods=['POST'])
def get_all_devices():
    uuid = request.form.get('uuid')

    device = Device.query.filter(Device.uuid == uuid).first
    if device is None:
        return to_error_json("No Devices Registered")
    return jsonify(device.dict())
