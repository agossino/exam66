from django.urls import include, path

from . import views

urlpatterns = [
    path("", views.HomeView.as_view(), name="home"),
    path("accounts/", include("django.contrib.auth.urls")),
    path("mcquestions/", views.list_mc_questions, name="ls_mcquest"),
    # for test purpose
    path("mdn", views.mdn, name="mdn"),
]
