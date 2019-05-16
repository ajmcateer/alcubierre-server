import functools
import hashlib
import datetime
from os import urandom
from return_status import to_error_json, to_success_json
from models.channel import Channel
from sqlalchemy import text

from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for, jsonify
)

from shared import db

bp = Blueprint('channels', __name__, url_prefix='/channels')


@bp.route('/create', methods=['POST'])
def register():
    name = request.form.get('name')
    icon = request.form.get('icon')

    if not name:
        return to_error_json("name is required")
    elif Channel.query.filter(Channel.name == name).first() is not None:
        return to_error_json("name {} is already in use".format(name))

    channel = Channel(name=name, icon=icon)
    db.session.add(channel)
    db.session.commit()
    return jsonify(channel.dict(True))


@bp.route('/', methods=['GET'], strict_slashes=False)
def get_channels():
    name = request.args.get('name')

    if name is None:
        return to_error_json("Name is required to find Channel")

    channel = Channel.query.filter(Channel.name == name).first()

    if channel is not None:
        return jsonify(channel.dict(False))
    else:
        return to_error_json("Channel {} does not exist".format(name))


@bp.route('/delete', methods=['POST'])
def delete_channels():
    name = request.form.get('name')
    admin_key = request.form.get('admin_key')

    if name is None:
        return to_error_json("name is missing")
    elif admin_key is None:
        return to_error_json("admin key is missing")

    channel = Channel.query.filter(Channel.name == name, Channel.admin_key == admin_key).first()

    if channel is not None:
        Channel.delete(channel)
        return to_success_json("Channel Deleted")
    else:
        return to_error_json("Channel or admin key mismatch")
