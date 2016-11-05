from consts import file_type
from abstract import Scan_condition

class Video_condition(Scan_condition): 

    def __init__(self):
        Scan_condition.__init__(self)
        self.mimes = {'.avi': 'video/x-msvideo', '.m4v': 'video/x-m4v', '.asf': 'video/x-ms-asf',
            '.wmv': 'video/x-ms-wmv', '.mpeg': 'video/mpeg', '.mp4': 'video/mp4', '.ogv': 'video/ogg',
            '.webm': 'video/webm', '.mkv': 'video/x-matroska'}

    def check_condition(self, extension):
        if extension in self.mimes:
            self.type = file_type['Video']
            self.writeable = True
            self.mime = self.mimes[extension]
            return True

        return False