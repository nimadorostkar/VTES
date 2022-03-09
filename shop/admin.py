from django.contrib import admin
from mptt.admin import MPTTModelAdmin, DraggableMPTTAdmin, TreeRelatedFieldListFilter
from django.contrib.admin.models import LogEntry
from . import models
from .models import Category, Shop, Product, Attributes









#------------------------------------------------------------------------------
class ShopAdmin(admin.ModelAdmin):
    list_display = ('name','short_description', 'category', 'date_created','logo_tag')
    list_filter = ("category","date_created")
    search_fields = ['name',]
    raw_id_fields = ('category'),
admin.site.register(models.Shop, ShopAdmin)







#------------------------------------------------------------------------------
 #https://django-mptt.readthedocs.io/en/latest/admin.html#mptt-admin-draggablempttadmin
class CategoryMPTTModelAdmin(MPTTModelAdmin, TreeRelatedFieldListFilter):
    mptt_level_indent = 15   # specify pixel amount for this ModelAdmin only
    mptt_indent_field = "name"
    search_fields=['name__name']
admin.site.register(models.Category, DraggableMPTTAdmin,
    list_display=('tree_actions', 'indented_title'),
    list_filter = ('parent',),
    raw_id_fields = ('parent',),
    search_fields=['name__name'],
    list_display_links=('indented_title',),)








#------------------------------------------------------------------------------
class AttributesAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ['name',]
admin.site.register(models.Attributes, AttributesAdmin)







#------------------------------------------------------------------------------
class ProductAdmin(admin.ModelAdmin):
    list_display = ('img_tag', 'name', 'provider_shop', 'price', 'category', 'date_created', 'available','approved')
    list_filter = ("category", "date_created", "available", "approved", "provider_shop")
    search_fields = ['name', 'code']
admin.site.register(models.Product, ProductAdmin)












#End
