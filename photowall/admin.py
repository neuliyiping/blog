from django.contrib import admin
from .models import Photos


@admin.register(Photos)
class PhotosConfig(admin.ModelAdmin):
    list_display = ('title','desc', 'image','isshow')

