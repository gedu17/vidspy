from app import db

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    password = db.Column(db.String(255))
    active = db.Column(db.Integer)
    level = db.Column(db.Integer)
    session_hash = db.Column(db.String(255))
 
    def __init__(self, name, password, active, level):
        self.name = name
        self.password = password
        self.active = active
        self.level = level
    
    def __repr__(self):
        return '<User %r: %r>' % (self.id, self.name)