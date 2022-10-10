from django.contrib import admin
from . import models







#------------------------------------------------------------------------------
class PostWayAdmin(admin.ModelAdmin):
    list_display = ('way','price')
    list_filter = ("way",)
admin.site.register(models.PostWay, PostWayAdmin)







#------------------------------------------------------------------------------
class AddressAdmin(admin.ModelAdmin):
    list_display = ('place','address', 'phone_number', 'user')
    list_filter = ("user", "place")
    search_fields = ['address', 'phone_number', 'postal_code']
    raw_id_fields = ('user'),
admin.site.register(models.Address, AddressAdmin)













#------------------------------------------------------------------------------
class CartAdmin(admin.ModelAdmin):
    list_display = ('user', 'product', 'quantity' )
    list_filter = ("user", )
    raw_id_fields = ['user', 'product']
admin.site.register(models.Cart, CartAdmin)











#------------------------------------------------------------------------------
class OrderAdmin(admin.ModelAdmin):
    list_display = ('code', 'total', 'status', 'pay_way', 'user')
    list_filter = ("status", "pay_way", "create_at", "update_at")
    search_fields = ['code', 'phone_number', 'postal_code']
    raw_id_fields = ['user', 'address', 'carts']
admin.site.register(models.Order, OrderAdmin)











#------------------------------------------------------------------------------
class DetermineAvailabilityAdmin(admin.ModelAdmin):
    list_display = ('cart', 'order', 'status')
    list_filter = ("status", "order")
    raw_id_fields = ['cart', 'order']
admin.site.register(models.DetermineAvailability, DetermineAvailabilityAdmin)












#End
