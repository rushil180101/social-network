from django.urls import path
from .views import *


urlpatterns = [
    path('my-profile', my_profile, name='my-profile'),
    path('my-profile/received-invites/', received_invitations_view, name='my-received-invites'),
    path('my-profile/available-profiles-to-invite/', available_profiles_to_invite, name='available-profiles-to-invite'),
]
