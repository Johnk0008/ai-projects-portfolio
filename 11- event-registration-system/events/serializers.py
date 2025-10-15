from rest_framework import serializers
from .models import Event, Registration

class EventSerializer(serializers.ModelSerializer):
    available_seats = serializers.ReadOnlyField()
    is_full = serializers.ReadOnlyField()
    
    class Meta:
        model = Event
        fields = [
            'id', 'title', 'description', 'event_type', 'date', 
            'venue', 'max_attendees', 'current_attendees', 
            'available_seats', 'is_full', 'price', 'image', 
            'is_active', 'created_at'
        ]

class RegistrationSerializer(serializers.ModelSerializer):
    event_title = serializers.CharField(source='event.title', read_only=True)
    event_date = serializers.DateTimeField(source='event.date', read_only=True)
    
    class Meta:
        model = Registration
        fields = [
            'id', 'event', 'event_title', 'event_date', 'first_name', 
            'last_name', 'email', 'phone', 'company', 'position',
            'dietary_restrictions', 'special_requirements',
            'registration_date', 'is_confirmed', 'confirmation_code'
        ]
        read_only_fields = ['registration_date', 'confirmation_code']
    
    def validate(self, data):
        event = data.get('event')
        email = data.get('email')
        
        # Check if event is active
        if not event.is_active:
            raise serializers.ValidationError("This event is not active for registration.")
        
        # Check if event is full
        if event.is_full():
            raise serializers.ValidationError("This event is fully booked.")
        
        # Check for duplicate registration
        if Registration.objects.filter(event=event, email=email).exists():
            raise serializers.ValidationError("You have already registered for this event.")
        
        return data
    
    def create(self, validated_data):
        registration = super().create(validated_data)
        # Update event attendee count
        registration.event.current_attendees += 1
        registration.event.save()
        return registration