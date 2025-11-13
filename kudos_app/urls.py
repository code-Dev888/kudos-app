from django.urls import path
from .views import AllUsersView, UserListView, LoginView, GiveKudoView, KudosReceivedView, RemainingKudosView

urlpatterns = [
    path("auth/login/", LoginView.as_view(), name="login"),
    path("users/", AllUsersView.as_view(), name="all-users"),
    path("users/<uuid:user_id>/", UserListView.as_view(), name="user-list"),
    path("kudos/give/<uuid:sender_id>/", GiveKudoView.as_view(), name="give-kudo"),
    path("kudos/received/<uuid:user_id>/", KudosReceivedView.as_view(), name="received-kudos"),
    path("kudos/remaining/<uuid:user_id>/", RemainingKudosView.as_view(), name="remaining-kudos"),
]