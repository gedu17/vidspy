from app import db
from time import time

class System_message(db.Model):
    __tablename__ = 'system_messages'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    message = db.Column(db.Text)
    read = db.Column(db.Integer)
    severity = db.Column(db.Integer)
    timestamp = db.Column(db.Integer)
    long_message = db.Column(db.Text)

    def __init__(self, user_id, message, severity, timestamp=int(time()), long_message=None, id=0):
        self.user_id = user_id
        self.message = message
        self.read = 0
        self.severity = severity
        self.timestamp = timestamp
        self.long_message = long_message
        if id is not 0:
            self.id = id
    
    def __repr__(self):
        return '<System_message %r for user %r: %r>' % (self.id, self.user_id, self.message)