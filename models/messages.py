from shared import db
from datetime import datetime


class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    channel_name = db.Column(db.String(120), unique=False, nullable=False)
    title = db.Column(db.TEXT, unique=False, nullable=False)
    message = db.Column(db.TEXT, unique=False, nullable=False)
    created_date = db.Column(db.TIMESTAMP, default=datetime.utcnow)

    def __init__(self, channel_name, title, message):
        self.channel_name = channel_name
        self.title = title
        self.message = message
        self.created_date = datetime.utcnow()

    def dict(self):
        sub = {
            "channel_name": self.channel_name,
            "title": self.title,
            "message": self.message,
            "created": int((self.created_date - datetime.utcfromtimestamp(0)).total_seconds()),
        }

        return sub
