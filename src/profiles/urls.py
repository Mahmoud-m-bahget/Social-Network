from django.urls import path
from .views import (my_profile_view , 
                    invites_received_view , 
                    profiles_list_view ,
                    ProfileDetailView,
                    invite_profiles_list_view,
                    ProfileListView,
                    send_invatations,
                    remove_from_friends,
                    accept_invatations,
                    reject_invatations,
                    )

app_name = 'profiles'

urlpatterns = [
    path('' , ProfileListView.as_view() , name = 'all-profiles-view'),
    path('myprofile/' , my_profile_view , name = 'my_profile_view'),
    path('my-invites/' , invites_received_view , name = 'my-invites-view'),
    path('to-invite/' , invite_profiles_list_view , name = 'invite-profiles-view'),
    path('send-invite/' , send_invatations , name = 'send-invite'),
    path('remove-friend/' , remove_from_friends , name = 'remove-friend'),
    path('<slug>/' , ProfileDetailView.as_view() , name = 'profile-detail-view'),
    path('my-invites-reject/' , reject_invatations , name = 'reject-invites'),
    path('my-invites-accept/' , accept_invatations , name = 'accept-invites'),
]