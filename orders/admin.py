from django.contrib import admin
from .models import Order, OrderItem

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    raw_id_fields = ['product']
    extra = 1


class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'first_name', 'last_name', 'number', 'city', 'post', 'number_of_post',
        'paid', 'data_create']
    list_filter = ['paid', 'data_create', 'city', ]
    inlines = [OrderItemInline, ]

admin.site.register(Order, OrderAdmin)