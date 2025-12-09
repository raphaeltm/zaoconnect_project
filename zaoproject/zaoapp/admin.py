from django.contrib import admin
from django.utils.html import format_html

from .models import Contact, Product


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'stock', 'is_active', 'created_at', 'image_thumb')
    list_filter = ('is_active', 'created_at')
    search_fields = ('name',)
    ordering = ('-created_at',)
    fields = ('name', 'description', 'price', 'stock', 'is_active', 'image', 'image_preview', 'created_at', 'updated_at')
    readonly_fields = ('image_preview', 'created_at', 'updated_at')

    def image_thumb(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="width:48px;height:48px;object-fit:cover;border-radius:4px;" />', obj.image.url)
        return '—'
    image_thumb.short_description = 'Image'

    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="max-width:200px;border-radius:8px;" />', obj.image.url)
        return 'No image uploaded'
    image_preview.short_description = 'Preview'


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'created_at')
    search_fields = ('name', 'email')