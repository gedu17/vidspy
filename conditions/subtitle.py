from consts import file_type
from abstract import Scan_condition

class Subtitle_condition(Scan_condition): 

    def __init__(self):
        Scan_condition.__init__(self)
        self.mimes = {'.srt': 'application/x-subrip', '.ssa': 'application/octet-stream',
            '.ass': 'application/octet-stream', '.smi': 'application/smil+xml', 
            '.sub': 'text/vnd.dvb.subtitle', '.idx': 'application/octet-stream', 
            '.mpl': 'application/octet-stream', '.vtt': 'text/vtt', 
            '.psb': 'application/vnd.3gpp.pic-bw-small', '.sami': 'application/octet-stream',
            '.pjs': 'application/octet-stream'}

    def check_condition(self, extension):
        if extension in self.mimes:
            self.type = file_type['Subtitle']
            self.writeable = False
            self.mime = self.mimes[extension]
            return True

        return False