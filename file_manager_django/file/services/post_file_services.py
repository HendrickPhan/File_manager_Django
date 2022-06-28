from app.models import App
from file.models import File
from hashlib import sha256
from datetime import datetime, timedelta
from django.conf import settings
from django.core.files.storage import default_storage
import uuid 
import magic

class PostFileServices:
    REQUIRED_FIELDS = ['file', 'app_id', 'secure_code', 'upload_time']
    IMAGES_EXTENSIONS = set(['pdf', 'png', 'jpg', 'jpeg'])
    VIDEOS_EXTENSIONS = set(['mp4','flv','wmv','mov','webm','mkv','vob','ogv','ogg','drc','gif','gifv','mng','avi','amv','m4p','m4v','3gp','f4v'])
    MAX_FILE_SIZE = 60 * 1000000
    DEFAULT_FILE_NAME = "default"

    def __init__(self, data):
        self.data = data

    def is_valid(self):
        # required fields
        if(not self.check_required_fields()):
            return False
        # check app id
        if(not self.check_app_exist()):
            return False
        #check_date_time
        # if(not self.check_date_time()):
        #     return False
        # check image
        if(not self.check_file()):
            return False
        # check secure code
        if(settings.NEED_CHECK_SECURECODE):
            if(not self.check_secure_code()):
                return False
        return True
    
    def check_required_fields(self):
        for required_field in self.REQUIRED_FIELDS:
            if(not required_field in self.data):
                self.error = 'Missing ' + required_field
                return False
        return True

    def check_app_exist(self):
        try:
            self.app = App.objects.get(id=self.data['app_id'])
        except:
            self.error = 'Invalid app'
            return False 
        return True 

    def check_date_time(self):
        try:
            self.upload_time = datetime.strptime(
                self.data['upload_time'], '%Y-%m-%d %H:%M:%S')
            current = datetime.now()
            if(self.upload_time + timedelta(minutes=10) < current 
                or self.upload_time > current):
                raise Exception()
        except:
            self.error = 'Invalid upload_time'
            return False 
        return True 
    
    def check_file(self):
        try:
            image = self.data['file']
            if( image.size > self.MAX_FILE_SIZE):
                raise Exception()
        except:
            self.error = 'Invalid file'
            return False 
        return True

    def check_secure_code(self):
        try:
            hash_str = "%s|%s|%s" % (
                self.data['app_id'], 
                self.data['upload_time'], 
                self.app.secret_key, ) 
            hashedWord = sha256(hash_str.encode('utf-8')).hexdigest()
            if(hashedWord != self.data['secure_code']):
                raise Exception()
        except:
            self.error = 'Invalid secure code'
            return False 
        return True 

    def _get_file_extension(self, file):
        mime = magic.from_buffer(file.read(), mime=True)
        extension = mime.rsplit('/', 1)[1].lower()
        return extension

    def generate_folder_name(self):
        return uuid.uuid4().hex[:6].lower() + '/'
        #TODO

    def save_file(self):
        extention = self._get_file_extension(self.data['file'])
        path = None
        if(extention in self.IMAGES_EXTENSIONS):
            self.type = 'image'
            path = self._save_file_to_path(self.data['file'], 'images/', extention)
        else:
            if(extention in self.VIDEOS_EXTENSIONS):
                self.type = 'video'
                path = self._save_file_to_path(self.data['file'], 'videos/', extention)
            else:
                self.type = 'file'
                path = self._save_file_to_path(self.data['file'], 'files/', extention)
        self.path = path
        return "%s://%s/file/%s"%(
            self.data['protocol'],
            self.data['domain'],
            path) 
    

    def _save_file_to_path(self, file, path, extension):
        folder_name = self.generate_folder_name() 
        new_path = (settings.MEDIA_ROOT + 
            path +
            folder_name +
            self.DEFAULT_FILE_NAME + 
            '.' + extension)
    
        file_name = default_storage.save(new_path, file)
        return (
            path +
            folder_name +
            extension)
    
    def create_record(self):
        file = File.objects.create(app = self.app, type = self.type, path=self.path, size=self.data['file'].size, hidden=self.data['hidden'])
        return file 
    
    def update_app_data(self):
        filesize = self.data['file'].size
        self.app.total_memory += filesize
        self.app.total_file += 1
        self.app.save()