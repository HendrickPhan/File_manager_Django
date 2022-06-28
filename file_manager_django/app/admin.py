from django.contrib import admin
from . import models
# Register your models here.
class AppAdmin(admin.ModelAdmin):
    exclude=('secret_key', 'total_file', 'total_memory', 'id')
    readonly_fields=('secret_key', 'total_file', 'total_memory', 'id')

admin.site.register(models.App, AppAdmin)
