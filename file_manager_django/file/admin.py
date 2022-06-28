from django.contrib import admin
from . import models
# Register your models here.
class FileAdmin(admin.ModelAdmin):
    def has_add_permission(self, request, obj=None):
        return False
    
    def changeform_view(self, request, object_id=None, form_url='', extra_context=None):
        extra_context = extra_context or {}
        extra_context['show_save_and_continue'] = False
        extra_context['show_save'] = False
        return super(FileAdmin, self).changeform_view(request, object_id, extra_context=extra_context)
    
    exclude=('app', 'path', 'size', 'type', 'uploaded_at')
    readonly_fields=('app', 'path', 'size', 'type', 'uploaded_at', 'image_fields')
    fields = ( 'app', 'path', 'size', 'type', 'uploaded_at', 'image_fields')
    

admin.site.register(models.File, FileAdmin)
