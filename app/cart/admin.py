from django.contrib import admin
from . import models









#------------------------------------------------------------------------------
class AddressAdmin(admin.ModelAdmin):
    list_display = ('place','address', 'phone_number', 'user')
    list_filter = ("user", "place")
    search_fields = ['address', 'phone_number', 'postal_code']
    raw_id_fields = ('user'),
admin.site.register(models.Address, AddressAdmin)







#------------------------------------------------------------------------------
class ShippingTimeAdmin(admin.ModelAdmin):
    list_display = ('date', )
    list_filter = ("date", )
admin.site.register(models.ShippingTime, ShippingTimeAdmin)









#------------------------------------------------------------------------------
class CartAdmin(admin.ModelAdmin):
    list_display = ('user', )
    list_filter = ("user", )
admin.site.register(models.Cart, CartAdmin)















#End
