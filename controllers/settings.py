from flask import Blueprint, g

settings_blueprint = Blueprint('settings_blueprint', __name__, template_folder='settings')

@settings_blueprint.route("/settings")
def index():
    from models import User
    from models import User_setting
    from os.path import expanduser, basename
    from os import sep
    from uuid import uuid4
    from classes import Base_scanner

    template = g._env.get_template('settings/settings.html')
    users = g._db.query(User)
    homedir = expanduser("~")
    selected_folders = []
    folders_in_db = g._db.query(User_setting).filter(User_setting.user_id == g._user.id).filter(User_setting.name == 'path').all()
    for folder in folders_in_db:
        selected_folders.append(folder.value)
    
    scanner = Base_scanner([])
    folders = scanner.scan({1: homedir})
    
    return template.render(user=g._user, users=users, folders=folders, 
           dir_separator=sep, selected_folders=selected_folders, uuid=uuid4, base_name=basename, page_title='Settings')

@settings_blueprint.route("/settings/user_paths", methods=['POST'])
def user_paths():
    from models import User_setting
    from models import Real_item
    from models import Virtual_item
    from classes import Advanced_scanner

    new_paths = []
    old_paths = []
    old_ids = {}
    paths = g._db.query(User_setting).filter(User_setting.user_id == g._user.id).filter(User_setting.name == 'path').all()

    for path in paths:
        old_ids[path.value] = path.id 
        old_paths.append(path.value)
    
    for item in g._request.json:
        new_paths.append(item['value'])

    items_to_remove = set(old_paths).difference(new_paths)
    items_to_add = set(new_paths).difference(old_paths)

    for real_path in items_to_remove:
        real_items = g._db.query(Real_item).filter(Real_item.user_path_id == old_ids[real_path]).all()
        if len(real_items) > 0:
            for real in real_items:
                virtual_item = g._db.query(Virtual_item).filter(Virtual_item.real_item_id == real.id).first()
                if virtual_item is not None:
                    g._db.delete(virtual_item)
                g._db.delete(real)

    for path in paths:
        if path.value in items_to_remove:
            g._db.delete(path)
    
    for path in items_to_add:
        new_item = User_setting(g._user.id, 'path', path, '')
        g._db.add(new_item)
    g._db.commit()

    scanner = Advanced_scanner(g._db, g._user)
    items = g._db.query(User_setting).filter(User_setting.user_id == g._user.id).filter(User_setting.name == 'path').all()
    to_scan = {}
    for item in items:
        to_scan[item.id] = item.value
    
    result = scanner.scan(to_scan)

    return 'OK'