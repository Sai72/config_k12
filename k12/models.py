import datetime

from django.db import models
from django.contrib.auth.models import User


class DailyActivity(models.Model):
    """
    This model is used for daily activity(attendance) of users
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.CharField(default="Absent", max_length=50, choices=(('Absent', 'Absent'), ('Present', 'Present')))
    login_date = models.DateField()
    login_hours = models.FloatField(default=0)

    def __str__(self):
        return f"{self.user} --> {self.login_date}"


class DayActivity(models.Model):
    """
    This model is used to maintain the day activity(login, logout) records of all users
    """
    date_id = models.ForeignKey(DailyActivity, on_delete=models.CASCADE)
    login_time = models.DateTimeField()
    logout_time = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.date_id}--{self.login_time}--{self.logout_time}"
