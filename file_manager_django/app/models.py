from django.db import models
import secrets
# Create your models here.
class App(models.Model):
    url = models.CharField(max_length=255)
    secret_key = models.CharField(max_length=34)
    total_file = models.PositiveIntegerField(default=0)
    total_memory = models.BigIntegerField(default=0)

    def __str__(self):
        return self.url
    
    def save(self, *args, **kwargs):
        if not self.id: # If true, this is being created. If false, this is just being edited and it already exists.
            # auto populate field_2
            self.secret_key = secrets.token_hex(16)
            self.total_file = 0
            self.total_memory = 0
        super(App, self).save(*args, **kwargs)