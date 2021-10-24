from django.contrib import admin
from analytics.models import Event

class EventAdmin(admin.ModelAdmin):
    search_fields = ['name', 'created_by__username']

admin.site.register(Event, EventAdmin)
