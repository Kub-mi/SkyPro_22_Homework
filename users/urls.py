from django.urls import path
from .views import SignUpView, CustomLoginView, ProfileUpdateView
from django.contrib.auth.views import LogoutView


urlpatterns = [
    path("signup/", SignUpView.as_view(), name="signup"),
    path("login/",  CustomLoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("profile/edit/", ProfileUpdateView.as_view(), name="profile_edit"),
]