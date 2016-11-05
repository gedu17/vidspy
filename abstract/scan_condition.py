from consts import file_type

class Scan_condition:

    def __init__(self):
        self.writeable = False
        self.type = file_type['None']
        self.mime = None

    def check_condition(self, extension):
        pass