from conditions import *
from flask import send_file, Response

class Video_viewer:

    def __init__(self, db, id, user_id, name, range):
        self.id = id
        self.user_id = user_id
        self.name = name
        self.range = range
        self.db = db
        self.video_condition = Video_condition()
        self.subtitle_condition = Subtitle_condition()
        self.packet_size = 64 * 1024 * 1024  # 64MB

    def video_exists(self):
        from models import Virtual_item
        from models import Real_item       
        from models import User_setting        

        item = self.db.query(Real_item).filter(Real_item.id == self.id).first()
        
        if item is not None:
            user_setting = self.db.query(User_setting).filter(User_setting.id == item.user_path_id).first()
            if user_setting is not None and user_setting.user_id == self.user_id:
                self.item = item
                return True
        return False

    def view(self):
        from os.path import splitext

        if self.video_exists():        
            ext = splitext(self.name)[1]   
            if self.video_condition.check_condition(ext):
                return self.view_video()
            elif self.subtitle_condition.check_condition(ext):
                return self.view_subtitle(ext)
        return 'Not Found', 404

    def view_subtitle(self, ext):
        from models import Real_item

        subtitle = self.db.query(Real_item).filter(Real_item.extension == ext).filter(Real_item.parent_id == self.item.parent_id) \
            .filter(Real_item.name == self.name).first()
        if subtitle is not None:
            return send_file(subtitle.path, self.subtitle_condition.mime)

        return 'Not Found', 404


    def view_video(self):
        from os import stat
        
        file = stat(self.item.path)
        self.file_size = file.st_size
        self.file_size_in_str = str(self.file_size-1)
        
        if self.range is not None:
            self.set_range()

            if self.left_side == -1:
                return self.no_start()
            elif self.right_side == -1:
                return self.no_end()
            else:
                return self.in_range()
        else:
            # Doesnt work currently, work around
            # return self.full_video()
            self.left_side = 0
            return self.no_end()

    def bad_range(self):
        response = Response('Range Not Satisfiable')
        response.status_code = 416
        response.content_range = 'bytes: */' + self.file_size_in_str
        response.content_length = 0
        return response

    def no_start(self):
        if self.right_side <= self.file_size:
            self.offset = self.file_size - self.right_side

            if self.right_side > self.packet_size:
                self.content_range = '%d-%d' % ((self.file_size - self.right_side), self.packet_size)
                self.count = self.packet_size
            else:
                self.content_range = '%d-%s' % ((self.file_size - self.left_side), self.file_size_in_str)
                self.count = self.right_side

            return self.return_video()
        return self.bad_range()

    def no_end(self):
        if self.left_side <= self.file_size:
            count = self.file_size - self.left_side
            self.offset = self.left_side
            if count > self.packet_size:
                self.content_range = '%d-%d' % (self.left_side, self.packet_size)
                self.count = self.packet_size
            else:
                self.content_range = '%d-%s' % (self.left_side, self.file_size_in_str)
                self.count = count
            
            return self.return_video()
        return self.bad_range()

    def in_range(self):
        if self.left_side <= self.file_size and self.right_side <= self.file_size:
            count = self.right_side - self.left_side + 1
            self.offset = self.left_side
            if count > self.packet_size:
                self.content_range = '%d-%d' % (self.left_side, self.packet_size)
                self.count = self.packet_size
            else:
                self.content_range = '%d-%d' % (self.left_side, self.right_side)
                self.count = count

            return self.return_video()
        return self.bad_range()
    
    def return_video(self):
        
        with open(self.item.path) as file:
            file.seek(self.offset)
            data = file.read(self.count)
            byte_array = bytearray(data)
            
            response = Response('Partial Content')
            response.status_code = 206
            response.content_length = self.count
            response.content_range = 'bytes ' + self.content_range + '/' + self.file_size_in_str
            response.content_type = self.video_condition.mime
            response.data = byte_array

            return response

    def set_range(self):
        self.left_side = -1
        self.right_side = -1
        
        if self.range is not None:
            range = self.range.replace('bytes=', '').replace('bytes: ', '').split('-')    
            if range[0] != '':
                self.left_side = long(range[0])
            
            if range[1] != '':
                self.right_side = long(range[1])

    
    def full_video(self):
        return send_file(self.item.path, self.video_condition.mime)

    