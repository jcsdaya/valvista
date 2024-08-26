from django.contrib import admin
from .models import Business
from .models import BusinessDetails

@admin.register(Business)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['username', 'password', 'email']

admin.site.register(BusinessDetails)
