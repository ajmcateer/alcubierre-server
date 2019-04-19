from shared import db
from datetime import datetime


class MessageQueue(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    channel_name = db.Column(db.String(120), unique=False, nullable=False)
    uuid = db.Column(db.String(40), unique=False, nullable=False)
    message_id = db.Column(db.Integer, unique=False, nullable=False)
    created_date = db.Column(db.TIMESTAMP, default=datetime.utcnow)

    def __init__(self, channel_name, uuid, message_id):
        self.channel_name = channel_name
        self.uuid = uuid
        self.message_id = message_id
        self.created_date = datetime.utcnow()

    def dict(self):
        sub = {
            "channel_name": self.channel_name,
            "uuid": self.uuid,
            "created": int((self.created_date - datetime.utcfromtimestamp(0)).total_seconds()),
        }

        return sub
