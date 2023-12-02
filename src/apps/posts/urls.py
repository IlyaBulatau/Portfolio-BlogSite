from django.urls import path, include

from apps.users.constants import USERNAME_LENGTH_MAX
from . import views


app_name = "posts"

urlpatterns = [
    path("<slug:slug>/", include(
        [
            path("", views.PostDetailView.as_view(), name="post_detail_view"),
            path("update/", views.PostUpdateView.as_view(), name="post_update_view"),
            ]
        )
    ),
    path("users/<slug:slug>/", views.PostUserListView.as_view(), name="post_user_view")
]
