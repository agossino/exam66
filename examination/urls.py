from django.urls import include, path

from . import views

urlpatterns = [
    path("", views.HomeView.as_view(), name="home"),
    path("accounts/", include("django.contrib.auth.urls")),
    path("questions/", views.view, name="view"),
]
