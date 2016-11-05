from flask import Blueprint, g

account_blueprint = Blueprint('account_blueprint', __name__)

@account_blueprint.route("/account/create", methods=['POST'])
def create():
    from models import User

    user = g._request.json['name'].lower().strip()
    password = g._request.json['password']
    level = int(g._request.json['level'])
    users = g._db.query(User).filter(User.name == user).first()

    if users is None:
        new_user = User(name=user, password=password, level=level, active=1)
        g._db.add(new_user)
        g._db.commit()
        return 'OK'
    
    return 'Bad Request', 400

@account_blueprint.route("/account/users", methods=['GET'])
def users():
    from models import User

    template = g._env.get_template('settings/manage_users.html')
    users = g._db.query(User)
    return template.render(users=users, user=g._user)
    
@account_blueprint.route("/account/delete/<int:id>", methods=['DELETE'])
def delete(id):
    from models import User, User_setting, Virtual_item, System_message

    user = g._db.query(User).filter(User.id == id).first()

    if user is None:
        return 'Bad Request', 400
    
    paths = g._db.query(User_setting).filter(User_setting.user_id == user.id).filter(User_setting.name == 'path')
    for path in paths:
        real_items = g._db.query(Real_item).filter(Real_item.user_path_id == path.id).all()
        for real_item in real_items:
            g._db.delete(real_item)
    
    virtual_items = g._db.query(Virtual_item).filter(Virtual_item.user_id == user.id).all()
    for virtual_item in virtual_items:
        g._db.delete(virtual_item)

    user_settings = g._db.query(User_setting).filter(User_setting.user_id == user.id).all()
    for user_setting in user_settings:
        g._db.delete(user_setting)

    system_messages = g._db.query(System_message).filter(System_message.user_id == user.id).all()
    for system_message in system_messages:
        g._db.delete(system_message)

    g._db.delete(user)
    g._db.commit()
    return 'OK'

@account_blueprint.route("/account/admin/<int:id>", methods=['PUT'])
def set_admin(id):
    from models import User

    value = int(g._request.json['value'])
    user = g._db.query(User).filter(User.id == id).first()

    if user is None:
        return 'Bad Request', 400
    
    user.level = 9 if value == 1 else 1
    g._db.commit()
    return 'OK'

@account_blueprint.route("/account/active/<int:id>", methods=['PUT'])
def set_active(id):
    from models import User

    value = int(g._request.json['value'])  
    user = g._db.query(User).filter(User.id == id).first()

    if user is None:
        return 'Bad Request', 400
    
    user.active = value
    g._db.commit()
    return 'OK'

@account_blueprint.route("/account/password", methods=['POST'])
def change_pasword():
    from models import User

    old_password = g._request.json['old_password']
    new_password = g._request.json['new_password']
    
    user = g._db.query(User).filter(User.id == g._user.id).first()

    if user is None or not verify_password(user, old_password):
        return 'Bad Request', 400

    user.password = generate_password(new_password)
    g._db.commit()
    return 'OK'

def verify_password(user, old_password):
    from models import User
    
    return user.password == old_password

def generate_password(new_password):
    return new_password