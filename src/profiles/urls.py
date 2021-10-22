from django.urls import path
from .views import *


urlpatterns = [
    path('my-profile', my_profile, name='my-profile'),
    path('my-profile/received-invites/', received_invitations_view, name='my-received-invites'),
    path('my-profile/my-friends/', friends_list, name='my-friends-list'),
    path('my-profile/pending-requests/', pending_requests, name='pending-requests'),
    path('my-profile/available-profiles-to-invite/', available_profiles_to_invite, name='available-profiles-to-invite'),
    path('send-invitation-to-add-friend', send_friend_request, name='send-friend-request'),
    path('remove-from-friends', remove_from_friends, name='remove-from-friends'),
]
