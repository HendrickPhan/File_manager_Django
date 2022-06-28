from app.models import App
from django.conf import settings
from django.core.files.storage import default_storage
from file.models import File

class DeleteFileServices:
    def __init__(self, app_id, id):
        self.app_id = app_id
        self.id = id

    def is_valid(self):  
        if (not self.checkSyntax()):
            self.error = 'Invalid Syntax'
            return False
        if (not self.checkExistFiles()):
            self.error = 'Invalid Files'
            return False
        return True
        
    def checkExistFiles(self):
        entry = File.objects.filter(app_id = self.app_id, id = self.id).count()
        if (entry == 0):
            return False
        return True

    def checkField(self):
        if self.app_id.isdigit() and self.id.isdigit():
            return True
        return False

    def deleteModels(self):
            return File.objects.get(app_id = self.app_id, id = self.id).delete()
            
        