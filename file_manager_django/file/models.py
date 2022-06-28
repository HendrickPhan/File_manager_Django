from django.db import models
from app.models import App
from django.conf import settings
from django.utils.safestring import mark_safe
from django.conf import settings
import shutil
# specifying choices 
  
FILE_TYPE = ( 
    ("image", "Image"), 
    ("video", "Video"), 
    ("file", "File"), 
) 
# Create your models here.
class File(models.Model):
    app = models.ForeignKey(App, on_delete=models.CASCADE)
    path = models.CharField(max_length=50)
    size = models.BigIntegerField(default=0)
    type = models.CharField(max_length = 20, choices = FILE_TYPE)
    hidden = models.BooleanField(default=False)
    uploaded_at = models.DateTimeField(auto_now_add=True, blank=True)

    def __str__(self):
        return self.path 

    def image_fields(self):
        if(self.type == 'image'):
            from django.utils.html import escape
            return mark_safe('<img width="400" src="%s" />' % escape('/file/' + self.path))
        return

    def delete(self):
        path = settings.MEDIA_ROOT + self.path
        #remove extension 
        path = path.rsplit('/', 1)[0]
        try:
            pass
            shutil.rmtree(path)
        except OSError as e:
            pass

        super(File, self).delete()