from django.contrib import admin
from .models import Song,FavouriteSong

# Register your models here.
admin.site.register(Song)
admin.site.register(FavouriteSong)
