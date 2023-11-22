from django.urls import path

from . import views


urlpatterns = [
    path("<slug:slug>/", views.ProfileDetailView.as_view(), name="profile_detail_view")
]