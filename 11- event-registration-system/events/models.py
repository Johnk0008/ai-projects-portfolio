from django.db import models
from django.core.validators import EmailValidator
import uuid

class Event(models.Model):
    EVENT_TYPES = [
        ('conference', 'Conference'),
        ('workshop', 'Workshop'),
        ('seminar', 'Seminar'),
        ('webinar', 'Webinar'),
        ('networking', 'Networking'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=200)
    description = models.TextField()
    event_type = models.CharField(max_length=20, choices=EVENT_TYPES)
    date = models.DateTimeField()
    venue = models.CharField(max_length=200)
    max_attendees = models.PositiveIntegerField()
    current_attendees = models.PositiveIntegerField(default=0)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    image = models.ImageField(upload_to='event_images/', null=True, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-date']
    
    def __str__(self):
        return self.title
    
    def available_seats(self):
        return self.max_attendees - self.current_attendees
    
    def is_full(self):
        return self.current_attendees >= self.max_attendees

class Registration(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='registrations')
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(validators=[EmailValidator()])
    phone = models.CharField(max_length=15)
    company = models.CharField(max_length=100, blank=True)
    position = models.CharField(max_length=100, blank=True)
    dietary_restrictions = models.TextField(blank=True)
    special_requirements = models.TextField(blank=True)
    registration_date = models.DateTimeField(auto_now_add=True)
    is_confirmed = models.BooleanField(default=False)
    confirmation_code = models.CharField(max_length=10, unique=True, blank=True)
    
    class Meta:
        ordering = ['-registration_date']
        unique_together = ['event', 'email']
    
    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.event.title}"
    
    def save(self, *args, **kwargs):
        if not self.confirmation_code:
            self.confirmation_code = self.generate_confirmation_code()
        super().save(*args, **kwargs)
    
    def generate_confirmation_code(self):
        import random
        import string
        return ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))