
from flask import Blueprint, g

real_item_blueprint = Blueprint('real_item_blueprint', __name__)

@real_item_blueprint.route('/real_item/<int:id>', methods=['DELETE'])
def delete(id):
    from models import Virtual_item, Real_item
    if id == 0:
        return 'Bad Request', 400
    try:
        recursive_real_delete(id)

        g._db.commit()
    except:
        return 'Bad Request', 400
    return 'OK'
    
def virtual_delete(id):
    from models import Virtual_item

    items = g._db.query(Virtual_item).filter(Virtual_item.real_item_id == id).all()
    for item in items:
        g._db.delete(item)

def recursive_real_delete(parent):
    from models import Real_item
    from consts import file_type
    from os import remove, rmdir

    items = g._db.query(Real_item).filter(Real_item.parent_id == parent).all()
    for item in items:
        if item.type == file_type['Folder']:
            recursive_real_delete(item.id)
        else:
            remove(item.path)
            g._db.delete(item)
        
        virtual_delete(item.id)
        
        
    
    parent_item = g._db.query(Real_item).filter(Real_item.id == parent).first()
    if parent_item is not None:
        g._db.delete(parent_item)
        if parent_item.type == file_type['Folder']:
            rmdir(parent_item.path)
        else:
            remove(parent_item.path)
    