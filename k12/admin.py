from django.contrib import admin
from .models import DailyActivity, DayActivity
from django.contrib.auth.models import User
# Register your models here.
from rest_framework.authtoken.models import Token

# admin.site.register(Token)
admin.site.register(DailyActivity)
admin.site.register(DayActivity)