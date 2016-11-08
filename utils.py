
def generate_virtual_items(item, parent, db, user_id, viewed, deleted, folders_only):
    from models import Virtual_item, Real_item
    from consts import file_type

    cursor = db.cursor()
    stmt = "SELECT * FROM `virtual_items` WHERE `user_id` = '%d' AND `parent_id` = '%d' AND `is_viewed` = '%d' AND `is_deleted` = '%d' ORDER BY `type`, `name`"
    cursor.execute(stmt % (user_id, parent, viewed, deleted))
    
    for virtual_item in cursor.fetchall():
        if not folders_only or (folders_only and virtual_item[9] == file_type['Folder']):
            real_id = 0
            real_path = ''
            real_extension = ''
            if virtual_item[2] is not None:
                cursor.execute("SELECT path, extension FROM `real_items` WHERE `id` = '%d' LIMIT 1" % (virtual_item[2]))
                real_item = cursor.fetchone()
                               
                real_id = virtual_item[2]
                real_path = real_item[0]
                real_extension = real_item[1]
            
            stmt = "SELECT COUNT(*) FROM `virtual_items` WHERE `user_id` = '%d' AND `parent_id` = '%d' AND `is_viewed` = '%d' AND `is_deleted` = '%d'"
            cursor.execute(stmt % (user_id, virtual_item[0], viewed, deleted))
            child_count = cursor.fetchone()[0]
            local_item = {'name': virtual_item[4], 'children': [], 'id': virtual_item[0], 'real_id': real_id, 'last': False, 'type': virtual_item[9], 
                'is_viewed': virtual_item[5], 'is_deleted': virtual_item[6], 'children_count': child_count, 
                'extension': real_extension, 'path': real_path }
            if virtual_item[9] == file_type['Folder']:
                generate_virtual_items(local_item, virtual_item[0], db, user_id, viewed, deleted, folders_only)
            item['children'].append(local_item)
    
    if len(item['children']) > 0 and parent != 0:
        item['children'][len(item['children'])-1]['last'] = True

def get_virtual_items(user_id, db, viewed=0, deleted=0, folders_only=False):
    from models import User_setting
    
    item = {'name': 'base', 'children': [], 'id': 0, 'last': False, 'type': 0, 'is_viewed': 0, 'is_deleted': 0, 'extension': '' }
    generate_virtual_items(item, 0, db, user_id, viewed, deleted, folders_only)
    return item

def get_real_items(user_id, db, paths, folders_only=False):
    from models import User_setting
    
    item = {'name': 'base', 'children': [], 'id': 0, 'last': False, 'type': 0, 'is_viewed': 0, 'is_deleted': 0, 'extension': '' }
    for path in paths:
        generate_real_items(item, path['id'], 0, db, user_id, folders_only)
    return item

def generate_real_items(item, path, parent, db, user_id, folders_only):
    from models import Real_item
    from consts import file_type

    cursor = db.cursor()
    stmt = "SELECT * FROM real_items WHERE `user_path_id` = '%s' AND `parent_id` = '%d' AND `type` < %d  ORDER BY `type`, `name`"
    cursor.execute(stmt % (path, parent, 2))
    for real_item in cursor.fetchall():
        if not folders_only or (folders_only and real_item[2] == file_type['Folder']):
            cursor.execute("SELECT COUNT(*) FROM real_items WHERE `user_path_id` = '%s' AND `parent_id` = '%d'" % (path, real_item[0]))
            child_count = cursor.fetchone()[0]
            local_item = {'name': real_item[4], 'children': [], 'id': real_item[0], 'last': False, 'type': real_item[2], 
                'is_viewed': 0, 'is_deleted': 0, 'children_count': child_count, 'extension': real_item[6] }
            if real_item[2] == file_type['Folder']:
                generate_real_items(local_item, path, real_item[0], db, user_id, folders_only)
            item['children'].append(local_item)
    
    if len(item['children']) > 0 and parent != 0:
        item['children'][len(item['children'])-1]['last'] = True
