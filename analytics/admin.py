from django.contrib import admin
from analytics.models import Event

# Register your models here.
class EventAdmin(admin.ModelAdmin):
    search_fields = ['name']


admin.site.register(Event, EventAdmin)
