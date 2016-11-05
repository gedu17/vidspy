
class Scan_item:

    def __init__(self, path, user_path_id, type, write_virtual_item):
        self.path = path
        self.user_path_id = user_path_id
        self.type = type
        self.write_virtual_item = write_virtual_item
        self.id = 0
        self.children = []