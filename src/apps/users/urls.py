from django.urls import path, include

from . import views


urlpatterns = [
    path("signup/", views.UserSingUpView.as_view(), name="signup_view"),
    path("login/", views.UserLogInView.as_view(), name="login_view"),
    path("logout/", views.UserLogoutView.as_view(), name="logout_view"),
]