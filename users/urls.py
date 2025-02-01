from django.urls import include, path
from . import views

urlpatterns = [
    path("dashboard/", views.dashboard, name="dashboard"),
    path("sign_up/", views.sign_up, name="sign_up"),
    path("accounts/", include("django.contrib.auth.urls")),
]
