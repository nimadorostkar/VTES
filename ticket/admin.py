from django.contrib import admin
from . import models
from .models import Ticket
from import_export.admin import ImportExportModelAdmin, ImportExportMixin








#------------------------------------------------------------------------------
class TicketAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ('subject', 'user')
    search_fields = ['subject', 'description']
    list_filter = ("user", 'subject')
    raw_id_fields = ('user'),
admin.site.register(models.Ticket, TicketAdmin)
