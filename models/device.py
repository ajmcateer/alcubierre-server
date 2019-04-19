from shared import db
from datetime import datetime


class Device(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    uuid = db.Column(db.String(40), unique=True, nullable=False)
    public_key = db.Column(db.String(120), unique=True, nullable=True)
    name = db.Column(db.String(120), unique=False, nullable=False)
    message_type = db.Column(db.String(120), unique=False, nullable=False)
    created_date = db.Column(db.TIMESTAMP, default=datetime.utcnow)

    def __init__(self, uuid, public_key, name, message_type):
        self.uuid = uuid
        self.public_key = public_key
        self.name = name
        self.message_type = message_type
        self.created_date = datetime.utcnow()

    def __repr__(self):
        return '<Device %r>' % self.uuid

    def dict(self):
        device = {
            "name": self.name,
            "uuid": self.uuid,
            "public_key": self.public_key,
            "message_type": self.message_type,
            "created": int((self.created_date - datetime.utcfromtimestamp(0)).total_seconds()),
        }

        return device
