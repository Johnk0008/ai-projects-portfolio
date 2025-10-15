from django.urls import path
from . import views

app_name = 'events'

urlpatterns = [
    # API Root
    path('', views.api_root, name='api-root'),
    
    # Event endpoints
    path('events/', views.EventListAPIView.as_view(), name='event-list'),
    path('events/<uuid:id>/', views.EventDetailAPIView.as_view(), name='event-detail'),
    path('events/<uuid:event_id>/stats/', views.event_stats, name='event-stats'),
    
    # Registration endpoints
    path('registrations/', views.RegistrationCreateAPIView.as_view(), name='registration-create'),
    path('registrations/<str:confirmation_code>/', views.RegistrationDetailAPIView.as_view(), name='registration-detail'),
    path('events/<uuid:event_id>/registrations/', views.EventRegistrationsAPIView.as_view(), name='event-registrations'),
]