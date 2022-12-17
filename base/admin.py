from django.contrib import admin
from django.contrib.admin import ModelAdmin

from base.models import Room, Message


class MessageAdmin(ModelAdmin):
    # ListView
    @staticmethod
    def cleanup_body(modeladmin, request, queryset):
        queryset.update(body="-- Deleted ---")

    ordering = ['id']
    list_display = ['id', 'body_short', 'room']
    list_display_links = ['id', 'body_short']
    list_per_page = 20
    list_filter = ['room']
    search_fields = ['body', 'id']
    actions = ['cleanup_body']

    fieldsets = [
        (
            None,
            {
                'fields': ['id', 'body']
            }
        ),
        (
            'Detail',
            {
                'fields': ['room', 'created', 'updated'],
                'description': 'Detailed Information about room.'
            }
        ),
        (
            'User Information',
            {
                'fields': ['user']
            }
        ),
    ]
    readonly_fields = ['id', 'created', 'updated']


class RoomAdmin(ModelAdmin):
    ordering = ['id']
    list_display = ['id', 'name', 'description']
    list_display_links = ['id', 'name']
    list_per_page = 20
    search_fields = ['name', 'description']

    fieldsets = [
        (
            None,
            {
                'fields': ['id', 'name', 'description'],
            }
        ),
        (
            'Detail',
            {
                'fields': ['participans', 'created', 'updated'],
                'description': 'Detailed Information about room.'
            }
        ),
    ]
    readonly_fields = ['id', 'created', 'updated']


admin.site.register(Room, RoomAdmin)
admin.site.register(Message, MessageAdmin)
