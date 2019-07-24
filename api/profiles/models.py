from django.db import models
# Create your models here.
from django_extensions.db.models import TimeStampedModel


class Profile(TimeStampedModel):
    user = models.OneToOneField('authentication.User', on_delete=models.CASCADE)
    bio = models.TextField(blank=True)
    image = models.URLField(blank=True)

    def __str__(self):
        return self.user.username
