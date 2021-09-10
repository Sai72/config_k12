from .models import DailyActivity, DayActivity
from rest_framework.authtoken.models import Token
from django.utils import timezone


def expire_users():
    """
    This function will acts as cron tab, It will get triggered automatically based on the configuration mentioned
    in settings.py file
    It will get the details all of activity's based on the null value in logout_time field at  dayActivity table and
    It will do logout the users based on the current time if it matched with end time
    """
    activities = DayActivity.objects.filter(logout_time__isnull=True)
    day_obj_list = []
    daily_obj_list = []
    user_ids = []
    for each in activities:
        login_hours = each.date_id.login_hours
        start_time = each.login_time
        duration = round((timezone.now() - start_time).seconds / 60 / 60, 1)
        if timezone.now().hour > 9:
            each.logout_time = timezone.now()
            day_obj_list.append(each)
            daily_obj = each.date_id
            daily_obj.login_hours = daily_obj.login_hours + duration
            daily_obj.status = "Present"
            daily_obj_list.append(daily_obj)
            user_ids.append(daily_obj.user_id)
    Token.objects.filter(user_id__in=user_ids).delete()
    DayActivity.objects.bulk_update(day_obj_list, ["logout_time"])
    DailyActivity.objects.bulk_update(daily_obj_list, ["login_hours", "status"])

