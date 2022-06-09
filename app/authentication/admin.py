from django.contrib import admin
from .models import User








#------------------------------------------------------------------------------
class UserAdmin(admin.ModelAdmin):
    list_display = ('mobile','company', 'img', 'is_legal')
    list_filter = ("email_verification", "is_legal")
    search_fields = ['mobile', "company"]
admin.site.register(User, UserAdmin)
