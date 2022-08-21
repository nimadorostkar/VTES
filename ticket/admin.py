from django.contrib import admin
from . import models
from .models import Ticket
from import_export.admin import ImportExportModelAdmin, ImportExportMixin








#------------------------------------------------------------------------------
class TicketAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ('title', 'user', 'status', 'type', 'answer_status', 'state')
    search_fields = ['title', 'description']
    list_filter = ('status', 'type', 'answer_status', 'state', 'title', "user")
    raw_id_fields = ('user'),
admin.site.register(models.Ticket, TicketAdmin)
