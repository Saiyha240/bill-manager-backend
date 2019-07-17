from django.contrib import admin

# Register your models here.
from api.users.models import User

admin.site.register(User)
