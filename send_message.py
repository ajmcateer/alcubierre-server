from models.subscription import Subscription
from models.device import Device
from models.message_queue import MessageQueue
from shared import db


def send_message(message, channel_name, admin_key):
    subscriptions = Subscription.query.filter_by(channel_name=channel_name).all()
    if subscriptions is not None:
        for sub in subscriptions:
            message_type = Device.query.with_entities(Device.message_type).filter_by(uuid=sub.uuid).one()
            if message_type[0] == "http":
                queued = MessageQueue(channel_name=channel_name, uuid=sub.uuid, message_id=message.id)
                db.session.add(queued)
                db.session.commit()

