from django.urls import path
from .views import *


urlpatterns = [
    path('my-profile', my_profile, name='my-profile'),
]
