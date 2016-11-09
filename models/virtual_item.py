from app import db

class Virtual_item(db.Model):
    __tablename__ = 'virtual_items'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    real_item_id = db.Column(db.Integer, db.ForeignKey('real_items.id'), nullable=True)
    parent_id = db.Column(db.Integer)
    name = db.Column(db.Text)
    viewed = db.Column(db.Integer)
    deleted = db.Column(db.Integer)
    viewed_time = db.Column(db.Integer)
    deleted_time = db.Column(db.Integer)
    type = db.Column(db.Integer)

    real_item = db.relationship('Real_item')


    def __init__(self, user_id, real_item_id, parent_id, name, type):
        self.user_id = user_id
        self.real_item_id = real_item_id
        self.parent_id = parent_id
        self.name = name
        self.type = type
        self.viewed = 0
        self.deleted = 0
        self.viewed_time = 0
        self.deleted_time = 0

    def __repr__(self):
        return '<Virtual_item %r: %r>' % (self.id, self.name)
