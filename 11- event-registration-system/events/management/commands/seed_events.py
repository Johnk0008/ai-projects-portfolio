from django.core.management.base import BaseCommand
from events.models import Event
from datetime import datetime, timedelta

class Command(BaseCommand):
    help = 'Seed the database with sample events'
    
    def handle(self, *args, **kwargs):
        events = [
            {
                'title': 'AI & Machine Learning Conference 2024',
                'description': 'Join us for the biggest AI and ML conference featuring top industry experts.',
                'event_type': 'conference',
                'date': datetime.now() + timedelta(days=30),
                'venue': 'Convention Center, Tech City',
                'max_attendees': 500,
                'price': 299.00
            },
            {
                'title': 'Python Web Development Workshop',
                'description': 'Hands-on workshop on building web applications with Django and FastAPI.',
                'event_type': 'workshop',
                'date': datetime.now() + timedelta(days=15),
                'venue': 'Innovation Hub, Downtown',
                'max_attendees': 50,
                'price': 99.00
            },
            {
                'title': 'Data Science Fundamentals Seminar',
                'description': 'Learn the fundamentals of data science and analytics.',
                'event_type': 'seminar',
                'date': datetime.now() + timedelta(days=7),
                'venue': 'Business Center, University District',
                'max_attendees': 100,
                'price': 0.00
            }
        ]
        
        for event_data in events:
            event, created = Event.objects.get_or_create(
                title=event_data['title'],
                defaults=event_data
            )
            if created:
                self.stdout.write(
                    self.style.SUCCESS(f'Created event: {event.title}')
                )