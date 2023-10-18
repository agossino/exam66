from django.urls import path

from . import views

urlpatterns = [
    path("", views.HomeView.as_view(), name="home"),
    # path("accounts/", include("django.contrib.auth.urls")),
    path("list_mcquestions/", views.MCQuestionListView.as_view(), name="ls_mcquest"),
    path(
        "detail_mcquestions/<int:pk>/",
        views.MCQuestionDetailView.as_view(),
        name="detail_mcquest",
    ),
    path(
        "form_mcquestions/<int:pk>/",
        views.MCQuestionFormView.as_view(),
        name="form_mcquest",
    ),
]
