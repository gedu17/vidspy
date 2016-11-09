from jinja2 import Template
from flask import Blueprint, g

item_blueprint = Blueprint('item_blueprint', __name__)

@item_blueprint.route('/item/move/<int:id>', methods=['PUT'])
def move(id):
    from models import Virtual_item, System_message
    from consts import severities

    if 'parent_id' in g._request.json:
        new_parent = int(g._request.json['parent_id'])
        item = g._db.query(Virtual_item).filter(Virtual_item.id == id).filter(Virtual_item.user_id == g._user.id).first()
        if item is not None:
            msg = System_message(g._user.id, ('Item %s succesfully moved from %d to %d.' % (item.name, item.parent_id, new_parent)), severities['Info'])
            g._db.add(msg)
            item.parent_id = new_parent
            g._db.commit()
            return 'OK'
    return 'Bad Request', 400
    
@item_blueprint.route('/item/edit/<int:id>', methods=['PUT'])
def edit(id):
    from models import Virtual_item, System_message
    from consts import severities

    if 'name' in g._request.json:
        new_name = g._request.json['name']
        item = g._db.query(Virtual_item).filter(Virtual_item.id == id).filter(Virtual_item.user_id == g._user.id).first()
        if item is not None:
            msg = System_message(g._user.id, ('Item %d succesfully edited from %s to %s.' % (id, item.name, new_name)), severities['Info'])
            g._db.add(msg)
            item.name = new_name
            g._db.commit()
            return 'OK'
    return 'Bad Request', 400

@item_blueprint.route('/item/create/', methods=['POST'])
def create():
    from models import Virtual_item, System_message
    from consts import file_type, severities
    if ('name' and 'parent') in g._request.json:
        name = g._request.json['name']
        parent = int(g._request.json['parent'])
        item = Virtual_item(g._user.id, None, parent, name, file_type['Folder'])
        msg = System_message(g._user.id, ('New Item with name %s and parent %d succesfully created.' % (name, parent)), severities['Info'])
        g._db.add(msg)
        g._db.add(item)
        g._db.commit()
    return 'OK'

@item_blueprint.route('/item/delete/<int:id>', methods=['DELETE'])
def delete(id):
    from models import Virtual_item, System_message
    from consts import severities
    from time import time

    item = g._db.query(Virtual_item).filter(Virtual_item.id == id).filter(Virtual_item.user_id == g._user.id).first()
    if item is not None:
        item.deleted = 1
        item.deleted_time = int(time()) 
        msg = System_message(g._user.id, ('Item %s succesfully flagged as deleted.' % (item.name)), severities['Info'])
        g._db.add(msg)
        g._db.commit()
        return 'OK'
    return 'Bad Request', 400

@item_blueprint.route('/item/undelete/<int:id>', methods=['PUT'])
def undelete(id):
    from models import Virtual_item, System_message
    from consts import severities
    from time import time

    item = g._db.query(Virtual_item).filter(Virtual_item.id == id).filter(Virtual_item.user_id == g._user.id).first()
    if item is not None:
        item.deleted = 0
        item.deleted_time = int(time())
        msg = System_message(g._user.id, ('Item %s succesfully flagged as not deleted.' % (item.name)), severities['Info'])
        g._db.add(msg)
        g._db.commit()
        return 'OK'
    return 'Bad Request', 400

@item_blueprint.route('/item/viewed/<int:id>', methods=['PUT'])
def viewed(id):
    from models import Virtual_item, System_message
    from consts import severities
    from time import time

    item = g._db.query(Virtual_item).filter(Virtual_item.id == id).filter(Virtual_item.user_id == g._user.id).first()
    if item is not None:
        item.viewed = 1
        item.viewed_time = int(time()) 
        msg = System_message(g._user.id, ('Item %s succesfully flagged as viewed.' % (item.name)), severities['Info'])
        g._db.add(msg)
        g._db.commit()
        return 'OK'
    return 'Bad Request', 400

@item_blueprint.route('/item/unviewed/<int:id>', methods=['PUT'])
def unviewed(id):
    from models import Virtual_item, System_message
    from consts import severities
    from time import time

    item = g._db.query(Virtual_item).filter(Virtual_item.id == id).filter(Virtual_item.user_id == g._user.id).first()
    if item is not None:
        item.viewed = 0
        item.viewed_time = int(time())
        msg = System_message(g._user.id, ('Item %s succesfully flagged as not viewed.' % (item.name)), severities['Info'])
        g._db.add(msg)
        g._db.commit()
        return 'OK'
    return 'Bad Request', 400

@item_blueprint.route('/item/view/<int:id>/<string:name>', methods=['GET'])
def view(id, name):
    from classes import Video_viewer

    video_viewer = Video_viewer(g._db, id, g._user.id,name, g._request.headers.get('range'))
    return video_viewer.view()
