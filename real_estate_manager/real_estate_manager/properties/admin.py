from django.contrib import admin
from django.utils.html import format_html

from .models import Property

@admin.register(Property)
class PropertyAdmin(admin.ModelAdmin):
    list_display = ("name", "owner", "property_type", "value", "display_image")
    search_fields = ('name', 'address', 'owner__username')
    list_filter = ('property_type', 'purchase_date')

    def owner_username(self, obj):
        return obj.owner.username
    owner_username.admin_order_field = 'owner__username'
    owner_username.short_description = 'Owner'

    def display_image(self, obj):
        if obj.image:
            return format_html(f'<img src="{obj.image.url}" style="height: 50px;"/>')
        return "No Image"

    display_image.short_description = "Image"
