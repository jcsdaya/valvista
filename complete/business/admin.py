from django.contrib import admin
from .models import Business
from .models import Business
from .models import Media

admin.site.register(Media)

@admin.register(Business)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['username', 'password', 'email']

