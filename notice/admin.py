from django.contrib import admin
from .models import PartnerExchangeNotice, ReturnedMoney
from import_export.admin import ImportExportModelAdmin, ImportExportMixin
from jalali_date import datetime2jalali, date2jalali
from jalali_date.admin import ModelAdminJalaliMixin, StackedInlineJalaliMixin, TabularInlineJalaliMixin




#------------------------------------------------------------------------------
class PartnerExchangeNoticeAdmin(ImportExportMixin, admin.ModelAdmin):
    list_display = ('exchange_partner', 'status', 'type')
    list_filter = ('exchange_partner', 'status', 'type')
    raw_id_fields = ('exchange_partner'),
admin.site.register(PartnerExchangeNotice, PartnerExchangeNoticeAdmin)




#------------------------------------------------------------------------------
class ReturnedMoneyAdmin(ImportExportMixin, admin.ModelAdmin):
    list_display = ('order', 'amount')
    list_filter = ('order',)
    raw_id_fields = ('order'),
admin.site.register(ReturnedMoney, ReturnedMoneyAdmin)
