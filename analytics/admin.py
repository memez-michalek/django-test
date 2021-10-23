from django.contrib import admin
from analytics.models import Event, User

class EventAdmin(admin.ModelAdmin):
    search_fields = ['name']

admin.site.register(Event, EventAdmin)
admin.site.register(User)