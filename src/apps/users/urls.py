from django.urls import path, include, re_path
from allauth.socialaccount import providers
from allauth.account import views as oauth_view
from allauth.socialaccount import views as social_view

from importlib import import_module

from . import views

oauth_urlpatterns = [
    #accoutn
    path("signup/", oauth_view.SignupView.as_view(template_name="users/oauth/oauth_signup.html"), name="account_signup"),
    path("login/", oauth_view.LoginView.as_view(template_name="users/oauth/oauth_login.html"), name="account_login"),
    path("logout/", oauth_view.logout, name="account_logout"),
    #email
    path("email/", oauth_view.email, name="account_email"),
    re_path(
        r"^confirm-email/(?P<key>[-:\w]+)/$",
        oauth_view.confirm_email,
        name="account_confirm_email",
    ),
    #social
    path("social/", include(
            [
            path("login/error/", social_view.LoginErrorView.as_view(template_name="users/oauth/oauth_login_error.html"), name="socialaccount_login_error"),
            path("signup/", social_view.SignupView.as_view(template_name="users/oauth/oauth_social_signup.html"), name="socialaccount_signup"),
            ]
        )
    ),

]

provider_urlpatterns = []
provider_classes = providers.registry.get_class_list()

# We need to move the OpenID Connect provider to the end. The reason is that
# matches URLs that the builtin providers also match.
provider_classes = [cls for cls in provider_classes if cls.id != "openid_connect"] + [
    cls for cls in provider_classes if cls.id == "openid_connect"
]
for provider_class in provider_classes:
    try:
        prov_mod = import_module(provider_class.get_package() + ".urls")
    except ImportError:
        continue
    prov_urlpatterns = getattr(prov_mod, "urlpatterns", None)
    if prov_urlpatterns:
        provider_urlpatterns += prov_urlpatterns

oauth_urlpatterns += provider_urlpatterns

urlpatterns = [
    path("signup/", views.UserSingUpView.as_view(), name="signup_view"),
    path("login/", views.UserLogInView.as_view(), name="login_view"),
    path("logout/", views.UserLogoutView.as_view(), name="logout_view"),
    
    path("oauth/", include(oauth_urlpatterns)),
]
