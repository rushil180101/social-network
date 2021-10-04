from django.urls import path
from .views import *


urlpatterns = [
    path('my-profile', my_profile, name='my-profile'),
    path('my-profile/received-invites/', received_invitations_view, name='my-received-invites'),
]
