""" This file will do business logic for API's"""
import pdb
from django.core import serializers
from django.shortcuts import render
from django.db import IntegrityError
from django.utils import timezone
from .models import DailyActivity, DayActivity
from rest_framework.response import Response
from django.http import HttpResponse
from rest_framework import permissions, viewsets
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from rest_framework.decorators import action
from rest_framework.parsers import JSONParser, FormParser, MultiPartParser
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime
import json


# Create your views here.


class UserAuthenticate(viewsets.ViewSet):
    """
    This user class will do Create, Login, Logout, List Users and List the Activity of particular user
    """
    parser_classes = (JSONParser, FormParser, MultiPartParser)

    @action(detail=False, methods=['POST'])
    def login(self, request):
        """
        This api will do login the user.
        1. If user tries to login before start time will allow the user and store day details and user details
        in dailyActivity table and based on the dailyActivity table will update the login time in dayActivity table.
        2. If User tries to login the first attempt after start time will not allow
        3. If user tries to login second or more attempts after start will allow
        methods: POST
        url: http://127.0.0.1:8000/k12/authenticate/login/
        headers: Content-Type: application/json
        Body: {"username": "username", "password": "password"}
        return token: Token
        """
        user = authenticate(username=request.data.get("username"), password=request.data.get("password"))
        if user is not None:
            today = timezone.now()
            try:
                daily_obj = DailyActivity.objects.get(user=user, login_date=today.date())
            except DailyActivity.DoesNotExist as e:
                daily_obj = DailyActivity.objects.create(user=user, login_date=today.today())
            if timezone.now().hour >= 6:
                day_obj = daily_obj.dayactivity_set.filter(date_id=daily_obj).last()
                if day_obj and day_obj.login_time.date() != today.date():
                    return Response({"message": "You cant login"})
            daily_obj.dayactivity_set.create(date_id=daily_obj, login_time=timezone.now())
            token, key = Token.objects.get_or_create(user=user)
            return Response({"token": token.key})

    @action(detail=False, methods=['GET'])
    def logout(self, request):
        """
        This api will logout the user and calculates the duration of last login and current logout time.
        If duration hours greatest to 9 hours, Will update the user day status and duration on DailyActivity table.
        Removes the Token once the logout is success.
        methods : GET
        headers : Authorization Token <token>
        url: http://127.0.0.1:8000/k12/authenticate/logout/
        return str: Logout success

        """
        if request.headers['Authorization'].startswith('Token'):
            user = Token.objects.get(key=request.headers['Authorization'].split()[-1]).user
            daily_obj = DailyActivity.objects.filter(user=user).last()
            day_obj = daily_obj.dayactivity_set.filter(date_id=daily_obj).last()
            day_obj.logout_time = timezone.now()
            day_obj.save()
            duration = round((day_obj.logout_time - day_obj.login_time).seconds / 60 / 60, 1)
            hour_info = daily_obj.login_hours + duration
            if hour_info > 9:
                daily_obj.status = "Present"
            daily_obj.login_hours = hour_info
            daily_obj.save()
            Token.objects.filter(user=user).delete()
            return Response({"message": "Logged out Successfully"})

    @action(detail=False, methods=['POST'])
    def register_user(self, request):
        """
        This api will do register the user(staff) on User table, id user is already exist it wll send proper response
        url: http://127.0.0.1:8000/k12/authenticate/register_user/
        headers: Content-Type: application/json
        Body: {"username": "username", "password": "password", "email":"emailid"}
        return: Response
        """
        try:
            User.objects.create_user(username=request.data.get("username"), password=request.data.get("password"),
                                     email=request.data.get("email"))
        except IntegrityError as e:
            return Response({"message": "User Already Exist"})
        return Response({"message": "Registered Successfully"})

    @action(detail=False, methods=['GET'])
    def user_attendance(self, request):
        """
        This api will list out the all users daily attendances and this api will work for day activity
         of particular user
        methods : GET
        headers: Content-Type: application/json
        url1: http://127.0.0.1:8000/k12/authenticate/user_attendance/ --> list out all users
        url2: http://127.0.0.1:8000/k12/authenticate/user_attendance/?id=2 --> list out particular user day activity
        return: JSON
        """
        pk = request.query_params.get('id', False)
        if not pk:
            user_list = DailyActivity.objects.all()
            user_json = serializers.serialize('json', user_list)
            return HttpResponse(user_json, content_type='application/json')
        else:
            day_activity = DayActivity.objects.filter(date_id=pk)
            day_activity_json = serializers.serialize('json', day_activity)
            login_count = day_activity.count()
            logout_count = day_activity.count()
            # import pdb;pdb.set_trace()
            if not day_activity:
                return Response({"Token": "User Not exists"})
            if not day_activity.last().logout_time:
                logout_count = login_count - 1
            update_data = json.loads(day_activity_json)
            update_data.insert(0, {"LoginCount": login_count, "LogoutCount": logout_count})
            return HttpResponse(json.dumps(update_data), content_type='application/json')
