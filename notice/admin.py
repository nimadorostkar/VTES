from django.contrib import admin
from .models import PartnerExchangeNotice
from import_export.admin import ImportExportModelAdmin, ImportExportMixin








#------------------------------------------------------------------------------
class PartnerExchangeNoticeAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ('exchange_partner', 'status', 'type')
    list_filter = ('exchange_partner', 'status', 'type')
admin.site.register(PartnerExchangeNotice, PartnerExchangeNoticeAdmin)
