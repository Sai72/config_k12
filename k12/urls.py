from django.urls import path, include
from django.conf.urls import url
from k12 import views
from django.views.decorators.csrf import csrf_exempt
# from k12.views import DailyActivityViewSet
from rest_framework.routers import DefaultRouter
router = DefaultRouter()
router.register('authenticate', views.UserAuthenticate,  basename='authenticate')


urlpatterns = router.urls