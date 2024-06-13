from django.urls import path
from .views import  SendFriendRequestView, ManageFriendRequestView, ListFriendsView, ListPendingFriendRequestsView
from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
urlpatterns = [
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('friend-request/send/', SendFriendRequestView.as_view(), name='send-friend-request'),
    path('friend-request/manage/', ManageFriendRequestView.as_view(), name='manage-friend-request'),
    path('friends/', ListFriendsView.as_view(), name='list-friends'),
    path('friend-requests/pending/', ListPendingFriendRequestsView.as_view(), name='list-pending-requests'),
]

