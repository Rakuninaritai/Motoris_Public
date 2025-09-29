from django.contrib import admin
# Register your models here.

from .models import EventPost,UploadImageModel
admin.site.register(EventPost)
admin.site.register(UploadImageModel)