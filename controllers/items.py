
from flask import Blueprint, g

items_blueprint = Blueprint('items_blueprint', __name__)

@items_blueprint.route('/items/scan/', methods=['GET'])
def scan():
    from classes import Advanced_scanner
    from models import User_setting
    from models import System_message
    from time import time
    from jinja2 import Template

    scanner = Advanced_scanner(g._db, g._user)
    items = g._db.query(User_setting).filter(User_setting.user_id == g._user.id).filter(User_setting.name == 'path').all()
    to_scan = {}
    for item in items:
        to_scan[item.id] = item.value
    
    result = scanner.scan(to_scan)

    return 'OK'