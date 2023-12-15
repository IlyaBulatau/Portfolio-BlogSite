from django.urls import path

from . import views

app_name = "core"

urlpatterns = [
    path("", view=views.HomePageView.as_view(), name="index_view"),
    path("/contacts", view=views.ContactPageView.as_view(), name="contacts_view")
    ]
