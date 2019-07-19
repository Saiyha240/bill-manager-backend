from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import ugettext_lazy as _


# Create your models here.

class UserManager(BaseUserManager):
    use_in_migrations = True

    def get_or_create_for_cognito(self, jwt_payload):
        cognito_username = jwt_payload['cognito:username']
        cognito_email = jwt_payload['email']
        cognito_sub = jwt_payload['sub']

        user, created = self.get_or_create(
            email=cognito_email
        )

        if created:
            user.cognito_sub = cognito_sub
            user.username = cognito_username
            user.save()

        return user

    def _create_user(self, username, email, password, **extra_fields):
        """
        Create and save a user with the given username, email, and password.
        """
        if not username:
            raise ValueError('The given username must be set')
        email = self.normalize_email(email)
        username = self.model.normalize_username(username)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, username, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(username, email, password, **extra_fields)

    def create_superuser(self, username, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(username, email, password, **extra_fields)


class User(AbstractUser):
    username = models.CharField(blank=True, null=True, max_length=20)
    email = models.EmailField(_('email address'), unique=True)
    cognito_sub = models.CharField(_('cognito sub'), max_length=34, unique=True, null=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    objects = UserManager()

    def __str__(self):
        return self.email
