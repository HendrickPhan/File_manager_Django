from app.models import App
from hashlib import sha256
from datetime import datetime, timedelta
from django.conf import settings
from django.core.files.storage import default_storage
from PIL import Image
import uuid 

class GetFileServices:

    SIZE = {
        'xl': 1280,
        'lg': 960,
        'md': 720,
        'sm': 480,
        'xs': 240,
        'avatar': 120,
    }

    def __init__(self, file_type, folder_name, extension, size):
        self.file_type = file_type
        self.folder_name = folder_name
        self.extension = extension
        self.size = size
        self.error = None
    
    def is_valid(self):
        return self.error is None

    def is_exist_default(self):
        path_storage = settings.MEDIA_ROOT + '%s/%s/default.%s'%(self.file_type, self.folder_name, self.extension)
        if (not default_storage.exists(path_storage)):
            return False
        return True

    def is_valid_size(self):
        return ( self.SIZE.get(self.size, False) 
            or self.size == 'default' )

    def get_file(self):
        if(self.file_type == 'files' or self.file_type == 'videos'):
            return self.get_default_file()

        if(self.file_type == 'images'):
            if(not self.is_valid_size()):
                self.error = 'Invalid size'
                return None

            if (self.size == 'default'):
                return self.get_default_file()
            else:
                return self.get_file_by_size()

    def get_default_file(self):
        path_url = '/media/%s/%s/default.%s' % (self.file_type, self.folder_name, self.extension)
        return path_url

    def get_file_by_size(self):
        if(not self.is_exist_default()):
            return self.get_default_file()

        path_url = '/media/%s/%s/%s.%s' % (
            self.file_type, 
            self.folder_name, 
            self.size, 
            self.extension)
        path_storage = settings.MEDIA_ROOT + '%s/%s/%s.%s'%(
            self.file_type, 
            self.folder_name, 
            self.size, 
            self.extension)

        if (not default_storage.exists(path_storage)):
            self.resize_and_save_image(path_storage)

        return path_url
    
    def resize_and_save_image(self, path_storage):
        default_path_storage = settings.MEDIA_ROOT + '%s/%s/default.%s'%(
                self.file_type, 
                self.folder_name, 
                self.extension)
        image = Image.open(default_path_storage)
        resize_image = self.resize_image(image, self.SIZE.get(self.size))
        resize_image.save(path_storage)
    
    def resize_image(self, image, newWidth):
        width, height = image.size
        newHeight = (int)(newWidth * height / width)
        resized_image = image.resize((newWidth, newHeight)) 
        return resized_image