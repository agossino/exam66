from django.urls import path

from . import views

urlpatterns = [
    path("", views.HomeView.as_view(), name="home"),
    path("list_mcquestions/", views.MCQuestionListView.as_view(), name="ls_mcquest"),
    path(
        "detail_mcquestions/<int:pk>/",
        views.MCQuestionDetailView.as_view(),
        name="detail_mcquest",
    ),
    path("start_exam/<int:issued_exam_id>/", views.start_exam, name="start_exam"),
    path("taking_exam/<int:pk>/", views.TakingExamView.as_view(), name="taking_exam"),
    path(
        "taking_exam/<int:pk>/<str:progress>/",
        views.TakingExamView.as_view(),
        name="exam_progress",
    ),
]
