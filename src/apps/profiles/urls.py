from django.urls import path, include

from . import views


app_name = "profiles"

urlpatterns = [
    path(
        "<slug:slug>/",
        include(
            [
                path("", views.ProfileDetailView.as_view(), name="profile_detail_view"),
                path(
                    "update/",
                    views.ProfileUpdateView.as_view(),
                    name="profile_update_view",
                ),
            ]
        ),
    ),
]
