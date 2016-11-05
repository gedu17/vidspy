from data_models import Scan_item
import os
import locale
from consts import file_type
locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')

class Base_scanner:

    def __init__(self, scan_conditions, ignore_hidden=True):
        self.ignore_hidden = ignore_hidden
        self.scan_conditions = scan_conditions

    def scan(self, dirs):
        items = []
        for id, dir in dirs.iteritems():
            base_dir = Scan_item(dir, id, 0, 0)
            self.__scan_dir(dir, id, base_dir)
            items.append(base_dir)
        return self.sort(items)

    def is_hidden(self, item):        
        if item[0] is '.' and self.ignore_hidden:
            return True
        
        return False
    
    def __scan_dir(self, dir_to_scan, dir_id, parent):
        for item in os.listdir(dir_to_scan):
            if not self.is_hidden(item):
                sep = os.sep if dir_to_scan[-1:] != os.sep else ''
                fullpath = dir_to_scan + sep + item

                if os.path.isdir(fullpath):
                    dir_item = Scan_item(fullpath, dir_id, file_type['Folder'], 1)
                    parent.children.append(dir_item)
                    self.__scan_dir(fullpath, dir_id, dir_item)
                    
                else:
                    ext = os.path.splitext(fullpath)[1]
                    for condition in self.scan_conditions:
                        if condition.check_condition(ext):
                            file_item = Scan_item(fullpath, dir_id, condition.type, int(condition.writeable))
                            parent.children.append(file_item)
                            break


    def sort(self, items):
        items.sort(cmp=self.compare)
        items.reverse()
        for item in items:
            self.sort(item.children)
        return items

    #UTILS#

    def print_object(self, item, ident):
        print self.print_spaces(ident) + item.path
        if item.children is not None:
            for it in item.children:
                print self.print_spaces(ident) + it.path
                for child in it.children:
                    if child.type == 0:
                        self.print_object(child, ident+1)
                    else:
                        print self.print_spaces(ident) + child.path
    
    def print_spaces(self, times):
        ret = ''
        i = 0
        while i <= times:
            ret += ' '
            i = i+1
        return ret

    def compare(self, item1, item2):
        res = [item1.path, item2.path]
        res.sort()
        if item1.type is file_type['Folder'] and item2.type is file_type['Folder']:
            return 1 if item1.path is res[0] else -1
        elif item1.type is file_type['Folder'] and item2.type is not file_type['Folder']:
            return 1
        elif item1.type is not file_type['Folder'] and item2.type is file_type['Folder']:
            return -1
        else:
            return 1 if item1.path is res[0] else -1