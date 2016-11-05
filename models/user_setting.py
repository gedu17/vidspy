from app import db

class User_setting(db.Model):
    __tablename__ = 'user_settings'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    name = db.Column(db.String(255))
    value = db.Column(db.String(255))
    description = db.Column(db.String(255))
 
    def __init__(self, user_id, name, value, description):
        self.user_id = user_id
        self.name = name
        self.value = value
        self.description = description
    
    def __repr__(self):
        return '<User_setting %r for user %r: %r = %r>' % (self.id, self.user_id, self.name, self.value)