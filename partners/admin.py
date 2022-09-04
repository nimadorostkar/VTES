from django.contrib import admin
from . import models
from .models import ExchangePartner, ExchangeReq
from import_export.admin import ImportExportModelAdmin, ImportExportMixin








#------------------------------------------------------------------------------
class ExchangePartnerAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ('user_shop', 'partner_shop', 'status')
    search_fields = ['user_shop', 'partner_shop']
    list_filter = ("user_shop", 'partner_shop')
admin.site.register(models.ExchangePartner, ExchangePartnerAdmin)
