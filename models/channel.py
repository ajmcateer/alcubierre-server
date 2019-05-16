import hashlib
from os import urandom

from shared import db
from datetime import datetime


class Channel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True, nullable=False)
    icon = db.Column(db.String(), unique=True, nullable=True)
    listen_key = db.Column(db.String(), unique=True, nullable=False)
    admin_key = db.Column(db.String(), unique=True, nullable=False)
    created_date = db.Column(db.TIMESTAMP, default=datetime.utcnow)

    def __init__(self, name, icon):
        self.name = name
        self.icon = icon
        self.created_date = datetime.utcnow()
        self.admin_key = hashlib.sha1(urandom(100)).hexdigest()[:32]
        self.listen_key = str(hashlib.sha1(self.admin_key.encode('utf-8')).hexdigest())[:40]

    def __repr__(self):
        return '<Channel %r>' % self.name

    def dict(self, show_admin):

        channel = {
            "name": self.name,
            "icon": self.icon,
            "listen_key": self.listen_key,
            "created": int((self.created_date - datetime.utcfromtimestamp(0)).total_seconds()),
        }

        if show_admin:
            channel["admin_key"] = self.admin_key

        return channel
