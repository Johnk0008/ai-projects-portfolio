from rest_framework import generics, status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse
from django.shortcuts import get_object_or_404
from .models import Event, Registration
from .serializers import EventSerializer, RegistrationSerializer

@api_view(['GET'])
def api_root(request, format=None):
    """
    API Root endpoint with links to all available endpoints
    """
    return Response({
        'message': 'Event Registration System API',
        'endpoints': {
            'events_list': reverse('events:event-list', request=request, format=format),
            'create_registration': reverse('events:registration-create', request=request, format=format),
        },
        'available_routes': [
            'GET /api/events/ - List all events',
            'GET /api/events/{id}/ - Get event details',
            'GET /api/events/{id}/stats/ - Get event statistics',
            'POST /api/registrations/ - Register for an event',
            'GET /api/registrations/{confirmation_code}/ - Get registration details',
            'GET /api/events/{event_id}/registrations/ - Get event registrations'
        ]
    })

class EventListAPIView(generics.ListAPIView):
    queryset = Event.objects.filter(is_active=True)
    serializer_class = EventSerializer
    
    def get_queryset(self):
        queryset = Event.objects.filter(is_active=True)
        event_type = self.request.query_params.get('type')
        if event_type:
            queryset = queryset.filter(event_type=event_type)
        return queryset

class EventDetailAPIView(generics.RetrieveAPIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    lookup_field = 'id'

class RegistrationCreateAPIView(generics.CreateAPIView):
    queryset = Registration.objects.all()
    serializer_class = RegistrationSerializer

class RegistrationDetailAPIView(generics.RetrieveAPIView):
    queryset = Registration.objects.all()
    serializer_class = RegistrationSerializer
    lookup_field = 'confirmation_code'

class EventRegistrationsAPIView(generics.ListAPIView):
    serializer_class = RegistrationSerializer
    
    def get_queryset(self):
        event_id = self.kwargs['event_id']
        event = get_object_or_404(Event, id=event_id)
        return Registration.objects.filter(event=event)

@api_view(['GET'])
def event_stats(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    total_registrations = event.registrations.count()
    confirmed_registrations = event.registrations.filter(is_confirmed=True).count()
    
    return Response({
        'event_title': event.title,
        'total_registrations': total_registrations,
        'confirmed_registrations': confirmed_registrations,
        'available_seats': event.available_seats(),
        'registration_rate': (event.current_attendees / event.max_attendees) * 100 if event.max_attendees > 0 else 0
    })