from django.urls import path

from . import views


app_name = "users"

urlpatterns = [
    path("signup/", views.UserSingUpView.as_view(), name="signup_view"),
    path("login/", views.UserLogInView.as_view(), name="login_view"),
    path("logout/", views.UserLogoutView.as_view(), name="logout_view"),

]