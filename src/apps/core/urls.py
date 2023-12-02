from django.urls import path

from . import views

app_name = "core"

urlpatterns = [path(route="", view=views.HomePageView.as_view(), name="index_view")]
