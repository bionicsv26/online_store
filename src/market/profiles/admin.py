from django.contrib import admin
from django.utils.html import format_html
from .models import Profile, Cart


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'full_name', 'phone', 'avatar', 'show_avatar']
    fields = ['user', 'full_name', ('phone', 'avatar')]
    raw_id_fields = ['user']
    readonly_fields = ['show_avatar']

    def show_avatar(self, obj):
        return format_html(f'<img src="{obj.avatar.url}" style="max-height: 100px;">')
    
    show_avatar.short_description = 'Аватар'


# временный объект
@admin.register(Cart)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'cost']
    fields = ['user', 'cost', 'seller_products', 'discount']
