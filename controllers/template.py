from jinja2 import Template
from flask import Blueprint, g
template_blueprint = Blueprint('template_blueprint', __name__)

@template_blueprint.route('/template/move/<int:id>', methods=['GET'])
def move(id):
    from models import Virtual_item
    from utils import get_virtual_items
    template = g._env.get_template('templates/move.html')
    item = get_virtual_items(g._user.id, g._db, True)
    virtual_item = g._db.query(Virtual_item).filter(Virtual_item.id == id).first()

    return template.render(items=item['children'], current_parent=virtual_item.parent_id, self_id=virtual_item.id)

@template_blueprint.route('/template/edit/<int:id>', methods=['GET'])
def edit(id):
    from models import Virtual_item
    
    template = g._env.get_template('templates/edit.html')
    virtual_item = g._db.query(Virtual_item).filter(Virtual_item.id == id).first()

    return template.render(value=virtual_item.name)

@template_blueprint.route('/template/create/', methods=['GET'])
def create():
    from utils import get_virtual_items
    template = g._env.get_template('templates/create.html')
    item = get_virtual_items(g._user.id, g._db, True)

    return template.render(items=item['children'])

@template_blueprint.route('/template/virtual_items/', methods=['GET'])
def virtual_items():
    from utils import get_virtual_items

    item = get_virtual_items(g._user.id, g._db)
    
    template = g._env.get_template('common/virtual_items.html')
    return template.render(user=g._user, item=item['children'], count=len(item['children']))

@template_blueprint.route('/template/viewed_items/', methods=['GET'])
def viewed_items():
    from utils import get_virtual_items

    item = get_virtual_items(g._user.id, g._db, 1, 0)
    template = g._env.get_template('common/viewed_items.html')
    return template.render(user=g._user, item=item['children'], count=len(item['children']))

@template_blueprint.route('/template/deleted_items/', methods=['GET'])
def deleted_items():
    from utils import get_virtual_items

    item = get_virtual_items(g._user.id, g._db, 0, 1)
    template = g._env.get_template('common/deleted_items.html')
    return template.render(user=g._user, item=item['children'], count=len(item['children']))

@template_blueprint.route('/template/important_system_messages')
def important_messages():
    from models import System_message
    from consts import severities, severity
    from datetime import datetime

    messages = g._db.query(System_message).filter(System_message.user_id == g._user.id).filter(System_message.severity >= severity) \
        .order_by(System_message.timestamp.desc()).all()
    template = g._env.get_template('common/system_messages_list.html')
    return template.render(user=g._user, count=len(messages), messages=messages, severities=severities, date_converter=datetime.fromtimestamp, listing_type=1)

@template_blueprint.route('/template/all_system_messages')
def all_messages():
    from models import System_message
    from consts import severities
    from datetime import datetime

    messages = g._db.query(System_message).filter(System_message.user_id == g._user.id).order_by(System_message.timestamp.desc()).all()
    template = g._env.get_template('common/system_messages_list.html')
    return template.render(user=g._user, count=len(messages), messages=messages, severities=severities, date_converter=datetime.fromtimestamp, listing_type=2)

@template_blueprint.route('/template/smbadge/<int:count>')
def smbadge(count):
    template = g._env.get_template('common/badge.html')
    return template.render(count=count)