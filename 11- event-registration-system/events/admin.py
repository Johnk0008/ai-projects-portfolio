from django.contrib import admin
from .models import Event, Registration

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ['title', 'event_type', 'date', 'venue', 'max_attendees', 'current_attendees', 'is_active']
    list_filter = ['event_type', 'is_active', 'date']
    search_fields = ['title', 'description', 'venue']
    readonly_fields = ['current_attendees', 'created_at', 'updated_at']

@admin.register(Registration)
class RegistrationAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'email', 'event', 'registration_date', 'is_confirmed']
    list_filter = ['event', 'is_confirmed', 'registration_date']
    search_fields = ['first_name', 'last_name', 'email', 'event__title']
    readonly_fields = ['registration_date', 'confirmation_code']