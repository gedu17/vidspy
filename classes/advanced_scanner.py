from classes import Base_scanner
from conditions import *
from data_models import Scan_item
from consts import file_type

class Advanced_scanner:

    def __init__(self, db, user):
        self.db = db
        self.result = {'new_items': [], 'deleted_items': [], 'new_items_count': 0, 'deleted_items_count': 0}
        self.user = user
        
    def scan(self, paths):
        conditions = [Video_condition(), Subtitle_condition()]
        base_scanner = Base_scanner(conditions)
        old_items = []
        for id, path in paths.iteritems():
            item = Scan_item(path, id, file_type['Folder'], 1)
            item.children = self.get_children(id, 0)
            old_items.append(item)
        
        new_items = base_scanner.scan(paths)

        new_items_func = lambda x: self.result['new_items'].append(x)
        deleted_items_func = lambda x: self.result['deleted_items'].append(x)

        self.find_difference(old_items, new_items, new_items_func)
        self.find_difference(new_items, old_items, deleted_items_func)

        for it in self.result['new_items']:
            self.add_items(it, 0, 0)

        for it in self.result['deleted_items']:
            self.remove_items(it)
        
        self.db.commit()

        self.generate_system_message()

        return self.result

    def find_difference(self, old_items, new_items, action):
        for i, new_item in enumerate(new_items):
            if not self.is_in_list(old_items, new_item.path):
                action(new_item)
            else:
                for j, new_item2 in enumerate(new_item.children):
                    if not self.is_in_list(old_items[i].children, new_item2.path):
                        action(new_item2)
                    if new_item2.type is file_type['Folder'] and len(old_items) >= i and len(old_items[i].children) >= j and j != 0:
                        self.find_difference(old_items[i].children[j].children, new_item2.children, action)

    def is_in_list(self, items, path):
        found = False
        for item in items:
            if item.path == path:
                found = True
                break
        
        return found   

    def get_real_item_id(self, path, user_path_id):
        from models import Real_item

        real_item = self.db.query(Real_item).filter(Real_item.path == path).filter(Real_item.user_path_id == user_path_id).first()
        if real_item is not None:
            return real_item.id
        raise "Real item with path %s and user path id %d does not exist" % (path, user_path_id)

    def get_virtual_item_id(self, id):
        from models import Virtual_item
        virtual_item = self.db.query(Virtual_item).filter(Virtual_item.real_item_id == id).filter(Virtual_item.user_id == self.user.id).first()
        if virtual_item is not None:
            return virtual_item.id
        raise "Virtual item with real item id %d and user id %d does not exist" % (id, self.user.id)

    def add_items(self, item, real_parent_id, virtual_parent_id):
        if real_parent_id is 0 and item.parent is None:
            real_parent_id = self.add_real_item(real_parent_id, item)
            if item.write_virtual_item:
                virtual_parent_id = self.add_virtual_item(real_parent_id, virtual_parent_id, item)
        else:
            rp_id = self.get_real_item_id(item.parent, item.user_path_id)
            vp_id = self.get_virtual_item_id(rp_id)
            real_parent_id = self.add_real_item(rp_id, item)
            if item.write_virtual_item:
                virtual_parent_id = self.add_virtual_item(real_parent_id, vp_id, item)

        for child in item.children:
            real_item = self.add_real_item(real_parent_id, child)
            virtual_item = 0
            if child.write_virtual_item:
                virtual_item = self.add_virtual_item(real_item, virtual_parent_id, child)
            
            if child.type is file_type['Folder']:
                self.add_items(child, real_item, virtual_item)
    
    def add_real_item(self, parent_id, item):
        from models import Real_item
        from os.path import basename, splitext

        real_item = self.db.query(Real_item).filter(Real_item.path == item.path).filter(Real_item.user_path_id == item.user_path_id).first()
        if real_item is not None:
            return real_item.id
        
        new_real_item = Real_item(parent_id, item.type, item.user_path_id, basename(item.path), item.path, splitext(item.path)[1])
        self.db.add(new_real_item)
        self.db.commit()
        self.result['new_items_count'] += 1
        return new_real_item.id

    def add_virtual_item(self, real_item_id, virtual_parent_id, item):
        from models import Virtual_item
        from os.path import basename, splitext

        name = item.path if item.path[-1:] is not '/' else item.path [-1:]
        virtual_item = self.db.query(Virtual_item).filter(Virtual_item.user_id == self.user.id).filter(Virtual_item.real_item_id == real_item_id).first()
        if virtual_item is not None:
            return virtual_item.id
        
        new_virtual_item = Virtual_item(self.user.id, real_item_id, virtual_parent_id, splitext(basename(name))[0], item.type)
        self.db.add(new_virtual_item)
        self.db.commit()

        return new_virtual_item.id

    def remove_items(self, item):
        from models import Virtual_item, Real_item

        if item.children is not None:
            for child in item.children:
                if child.type is file_type['Folder']:
                    self.remove_items(child)
                else:
                    virtual_item = self.db.query(Virtual_item).filter(Virtual_item.real_item_id == child.id).first()
                    if virtual_item is not None:
                        self.db.delete(virtual_item)
                    
                    real_item = self.db.query(Real_item).filter(Real_item.id == child.id).first()
                    if real_item is not None:
                        self.db.delete(real_item)
                        self.result['deleted_items_count'] += 1  

        virtual_item = self.db.query(Virtual_item).filter(Virtual_item.real_item_id == item.id).first()
        if virtual_item is not None:
            self.db.delete(virtual_item)                  
            
        real_item = self.db.query(Real_item).filter(Real_item.id == item.id).first()
        if real_item is not None:
            self.db.delete(real_item)
            self.result['deleted_items_count'] += 1    

    def get_children(self, user_path_id, parent_id):
        from models import Real_item
        result = []
        real_items = self.db.query(Real_item).filter(Real_item.parent_id == parent_id). \
            filter(Real_item.user_path_id == user_path_id).order_by(Real_item.type). \
            order_by(Real_item.path).all()

        for real_item in real_items:
            item = Scan_item(real_item.path, real_item.user_path_id, real_item.type, (1 if real_item.type != file_type['Subtitle'] else 0))
            item.id = real_item.id
            if item.type == file_type['Folder']:
                item.children = self.get_children(user_path_id, real_item.id)
            result.append(item)
        return result
    
    def generate_result(self, items, phrase):
        ret = '<div>'
        ret += '<h4>' + phrase + '</h4>'
        ret += '<ul class="list-group">'
        for item in items:
            ret += self.generate_diff(item, 1)
        ret += '</ul>'
        ret += '</div>'
        return ret

    def generate_diff(self, item, level):
        from consts import file_type
        pad = level * 10
        ret = '<li class="list-group-item" style="padding-left: ' + str(pad) + 'px;">' + item.path
        if item.type == file_type['Folder']:
            ret += '<span class="badge">'+ str(len(item.children)) + '</span>'
        
        ret += '</li>'
        if item.children is not None:
            for child in item.children:
                ret += self.generate_diff(child, level+1)
        return ret

    def generate_system_message(self):
        from models import System_message
        from time import time
        
        if self.result['new_items_count'] > 0:
            msg = System_message(self.user.id, ('%d items added.' % self.result['new_items_count']), 0, 1, 
                int(time()), self.generate_result(self.result['new_items'], 'New items'))
            self.db.add(msg)
        if self.result['deleted_items_count'] > 0:
            msg = System_message(self.user.id, ('%d items removed.' % self.result['new_items_count']), 0, 1, 
                int(time()), self.generate_result(self.result['deleted_items'], 'Removed items'))
            self.db.add(msg)

        self.db.commit()
