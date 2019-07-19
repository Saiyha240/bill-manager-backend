from django.contrib import admin

# Register your models here.
from api.events.models import Event, Guest

admin.register(Event)
admin.register(Guest)
