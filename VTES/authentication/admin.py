from django.contrib import admin
from django.contrib.admin.models import LogEntry
from . import models
from .models import Profile



admin.site.site_header= "VTES"
admin.site.site_title= "VTES"
admin.site.register(LogEntry)





#------------------------------------------------------------------------------
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user','phone','date_created')
    list_filter = ('date_created',)
    search_fields = ['user', 'phone']
admin.site.register(models.Profile, ProfileAdmin)
