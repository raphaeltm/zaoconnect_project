from django.contrib import admin
from django.utils.html import format_html

from .models import Contact, Product, Cart, CartItem


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


class CartItemInline(admin.TabularInline):
    model = CartItem
    extra = 0
    readonly_fields = ('product', 'quantity', 'created_at', 'updated_at')
    fields = ('product', 'quantity', 'created_at', 'updated_at')


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ('user', 'created_at', 'updated_at')
    search_fields = ('user__username', 'user__email')
    readonly_fields = ('created_at', 'updated_at')
    inlines = [CartItemInline]


@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ('cart', 'product', 'quantity', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('cart__user__username', 'product__name')
    readonly_fields = ('created_at', 'updated_at')
