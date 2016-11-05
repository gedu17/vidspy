from app import db
from models.virtual_item import Virtual_item

class Real_item(db.Model):
    __tablename__ = 'real_items'
    id = db.Column(db.Integer, primary_key=True)
    parent_id = db.Column(db.Integer)
    type = db.Column(db.Integer)
    user_path_id = db.Column(db.Integer)
    name = db.Column(db.Text)
    path = db.Column(db.Text) #, unique=True
    extension = db.Column(db.String(255))

    virtual_items = db.relationship(Virtual_item, backref='real_items', cascade='all, delete-orphan', lazy='dynamic')


    def __init__(self, parent_id, type, user_path_id, name, path, extension):
        self.parent_id = parent_id
        self.type = type
        self.user_path_id = user_path_id
        self.name = name
        self.path = path
        self.extension = extension
    
    def __repr__(self):
        return '<Real_item %r: %r (%r)>' % (self.id, self.name, self.path)
