from django.contrib import admin
from .models import Title, Level, Hashtag

# Register your models here.

admin.site.register(Title)
admin.site.register(Level)
admin.site.register(Hashtag)
