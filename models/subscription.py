from shared import db
from datetime import datetime
from .channel import Channel


class Subscription(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    uuid = db.Column(db.String(40), unique=False, nullable=False)
    channel_key = db.Column(db.String(120), unique=False, nullable=True)
    channel_name = db.Column(db.String(120), unique=False, nullable=True)
    last_viewed = db.Column(db.TIMESTAMP, default=datetime.utcnow)
    created_date = db.Column(db.TIMESTAMP, default=datetime.utcnow)

    def __init__(self, uuid, channel_key, channel_name):
        self.uuid = uuid
        self.channel_key = channel_key
        self.channel_name = channel_name
        self.last_viewed = datetime.utcnow()
        self.created_date = datetime.utcnow()

    def dict(self):
        sub = {
            "uuid": self.uuid,
            "channel_key": self.channel_key,
            "last_viewed": self.last_viewed,
            "created": int((self.created_date - datetime.utcfromtimestamp(0)).total_seconds()),
        }

        return sub
