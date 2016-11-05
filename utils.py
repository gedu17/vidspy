
def print_items(items):
    for key in items.iterkeys():
        items['name']
        for child in items['children']:
            print_items(child)

def generate_virtual_items(item, parent, db, user_id, viewed=0, deleted=0):
    from models import Virtual_item, Real_item
    from consts import file_type

    virtual_items = db.query(Virtual_item).filter(Virtual_item.user_id == user_id).filter(Virtual_item.parent_id == parent) \
        .filter(Virtual_item.is_viewed == viewed).filter(Virtual_item.is_deleted == deleted).order_by(Virtual_item.type).order_by(Virtual_item.name).all()
    
    for virtual_item in virtual_items:
        child_count = db.query(Virtual_item).filter(Virtual_item.user_id == user_id).filter(Virtual_item.parent_id == virtual_item.id).count()
        local_item = {'name': virtual_item.name, 'children': [], 'id': virtual_item.real_item.id, 'last': False, 'type': virtual_item.type, 
            'is_viewed': virtual_item.is_viewed, 'is_deleted': virtual_item.is_deleted, 'children_count': child_count, 
            'extension': virtual_item.real_item.extension }
        if virtual_item.type == file_type['Folder']:
            generate_virtual_items(local_item, virtual_item.id, db, user_id, viewed, deleted)
        item['children'].append(local_item)
    
    if len(item['children']) > 0 and parent != 0:
        item['children'][len(item['children'])-1]['last'] = True

def get_virtual_items(user_id, db, viewed=0, deleted=0):
    from models import User_setting
    
    item = {'name': 'base', 'children': [], 'id': 0, 'last': False, 'type': 0, 'is_viewed': 0, 'is_deleted': 0, 'extension': '' }
    generate_virtual_items(item, 0, db, user_id, viewed, deleted)
    return item

def get_real_items(user_id, db, paths, folders_only=False):
    from models import User_setting
    
    item = {'name': 'base', 'children': [], 'id': 0, 'last': False, 'type': 0, 'is_viewed': 0, 'is_deleted': 0, 'extension': '' }
    for path in paths:
        generate_real_items(item, path['id'], 0, db, user_id, folders_only)
    return item

def generate_real_items(item, path, parent, db, user_id, folders_only=False):
    from models import Real_item
    from consts import file_type

    real_items = db.query(Real_item).filter(Real_item.user_path_id == path).filter(Real_item.parent_id == parent) \
        .filter(Real_item.type < 2).order_by(Real_item.parent_id).all()
    for real_item in real_items:
        if not folders_only or (folders_only and real_item.type == file_type['Folder']):
            child_count = db.query(Real_item).filter(Real_item.user_path_id == path).filter(Real_item.parent_id == real_item.id).count()
            local_item = {'name': real_item.name, 'children': [], 'id': real_item.id, 'last': False, 'type': real_item.type, 
                'is_viewed': 0, 'is_deleted': 0, 'children_count': child_count, 'extension': real_item.extension }
            if real_item.type == file_type['Folder']:
                generate_real_items(local_item, path, real_item.id, db, user_id, folders_only)
            item['children'].append(local_item)
    
    if len(item['children']) > 0 and parent != 0:
        item['children'][len(item['children'])-1]['last'] = True