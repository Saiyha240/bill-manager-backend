from django.contrib import admin

# Register your models here.
from api.events.models import Event, EventUser

admin.register(Event)
admin.register(EventUser)
