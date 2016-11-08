from jinja2 import Template
from flask import Blueprint, g

home_blueprint = Blueprint('home_blueprint', __name__)

@home_blueprint.route('/')
def index():
    from utils import get_virtual_items

    item = get_virtual_items(g._user.id, g._sqldb)
    template = g._env.get_template('home.html')
    return template.render(user=g._user, item=item['children'], count=len(item['children']))

@home_blueprint.route('/physical')
def physical():
    from utils import get_real_items
    # from models import User_setting
    # from models import Real_item

    # user_paths = g._db.query(User_setting).filter(User_setting.user_id == g._user.id).filter(User_setting.name == 'path').all()
    cursor = g._sqldb.cursor()
    cursor.execute("SELECT id, value FROM user_settings WHERE `user_id` = '%d' AND `name` = '%s'" % (g._user.id, 'path'))
    paths = []
    for user_path in cursor.fetchall(): # user_paths:
        # count = g._db.query(Real_item).filter(Real_item.parent_id == 0).filter(Real_item.user_path_id == user_path.id) \
        #     .filter(Real_item.type < 2).count()
        # paths.append({'id': user_path.id, 'value': user_path.value, 'count': count})
        cursor.execute("SELECT COUNT(*) FROM real_items WHERE `parent_id` = '%d' AND `user_path_id` = '%d' AND `type` < %d" % (0, user_path[0], 2))
        count = cursor.fetchone()
        paths.append({'id': user_path[0], 'value': user_path[1], 'count': count[0]})

    item = get_real_items(g._user.id, g._sqldb, paths)
    template = g._env.get_template('physical.html')
    return template.render(user=g._user, item=item['children'], count=len(item['children']), paths=paths)
