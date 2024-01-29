from django.contrib import admin

from market.tags.models import Tag


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = 'pk', 'name'
    list_display_links = 'name',
