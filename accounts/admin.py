from django.contrib import admin
from accounts.models import Customer, Product, Order, Tag
# Register your models here.

admin.site.register(Customer)
admin.site.register(Product)
admin.site.register(Tag)

class OrderAdmin(admin.ModelAdmin):
    list_display = ('product','customer','status')



admin.site.register(Order , OrderAdmin)