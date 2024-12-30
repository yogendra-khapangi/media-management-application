from django.contrib import admin
from .models import *

# Register your models here.
class UploadedFileAdmin(admin.ModelAdmin):
    list_display = ["name", "size", "type", "date_uploaded", "category"]

admin.site.register(UploadedFile, UploadedFileAdmin)