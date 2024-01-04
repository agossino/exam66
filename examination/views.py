from datetime import datetime, timedelta
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render
from django.views.generic import (
    DetailView,
    ListView,
    TemplateView,
    UpdateView,
)
from http import HTTPStatus

from .models import IssuedExam, MultichoiceQuestion, SelectedQuestion
from .forms import EssayAnswerForm, MultichoiceForm
from .utils import user_get_401_or_none

# TODO Multichoice questions in basic examination stardard have a
# time allowed of 75 seconds per question. Essay question 20 minutes (1200 s).
# Multichoice questions in Aircraft Type Training examination stardard have
# a time allowed of 90 seconds per question.
SECONDS_PER_MULTICHOIICE_QUESTION = 75
SECONDS_PER_ESSAY_QUESTION = 1200

ALL_QUEST_IDS = "all_question_ids"
MULTICHOICE_QUEST_IDS = "multichoice_question_ids"
ESSAY_QUEST_IDS = "essay_question_ids"
QUEST_LIST_INDEX = "current_question_list_index"
LAST_LIST_INDEX = "last_question_list_index"
CURRENT = "current_question"


class HomeView(TemplateView):
    """Home view"""

    template_name = "examination/home.html"

    def get_context_data(self, **kwargs):
        context = super(HomeView, self).get_context_data(**kwargs)
        return context


class MCQuestionListView(PermissionRequiredMixin, ListView):
    permission_required = "examination.view_multichoicequestion"
    queryset = MultichoiceQuestion.valid_only.all()
    context_object_name = "questions"
    paginate_by = 3
    template_name = "examination/ls_mcquest.html"


class MCQuestionDetailView(PermissionRequiredMixin, DetailView):
    permission_required = "examination.view_multichoicequestion"
    template_name = "examination/detail.html"
    model = MultichoiceQuestion
    template_name = "examination/detail_mcquest.html"


def start_exam(request, issued_exam_id):
    """Start page for the given issued exam"""
    issued_exam = get_object_or_404(IssuedExam, pk=issued_exam_id)
    rebut_401 = user_get_401_or_none(request, issued_exam)
    if rebut_401 is not None:
        return rebut_401

    selected_questions = issued_exam.selectedquestion_set.all()
    question_count = selected_questions.count()
    if question_count > 0:
        request.session[ALL_QUEST_IDS] = [
            question.id for question in selected_questions
        ]
        multichoice_question_ids = [
            question.id for question in selected_questions.exclude(multichoice_ref=None)
        ]
        request.session[MULTICHOICE_QUEST_IDS] = multichoice_question_ids
        essay_question_ids = [
            question.id for question in selected_questions.exclude(essay_ref=None)
        ]
        request.session[ESSAY_QUEST_IDS] = essay_question_ids
        request.session[QUEST_LIST_INDEX] = 0
        request.session[LAST_LIST_INDEX] = len(request.session[ALL_QUEST_IDS]) - 1
    time_allowed = selected_questions.count() * SECONDS_PER_MULTICHOIICE_QUESTION
    return render(
        request,
        "examination/start_exam.html",
        {
            "issued_exam": issued_exam,
            "questions_count": question_count,
            "time_allowed": time_allowed,
        },
    )


class TakingExamView(PermissionRequiredMixin, UpdateView):
    """This class manages an examination session.
    It is called from start_exam.html with the IssuedExam pk in the url
    or from taking_exam.html with IssuedExam pk and progress in the url,
    a string that means which is the next SelectedQuestion to be showed."""

    permission_required = "examination.change_givenanswer"
    template_name = "examination/question_exam.html"
    fields = "__all__"
    model = IssuedExam
    form = None

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["current_issued_exam"] = self.kwargs.get(self.pk_url_kwarg)

        self.request.session.get(ALL_QUEST_IDS)

        current_question_id = self.request.session[ALL_QUEST_IDS][
            self.request.session[QUEST_LIST_INDEX]
        ]

        context[CURRENT] = SelectedQuestion.objects.get(id=current_question_id)
        context[QUEST_LIST_INDEX] = self.request.session[QUEST_LIST_INDEX]
        context[LAST_LIST_INDEX] = self.request.session[LAST_LIST_INDEX]

        return context

    def post(self, request, *args, **kwargs):
        selected_question_progress = self.kwargs.get("progress")

        self._get_answer()

        self.object = self.get_object()

        question_ids = self.request.session.get(ALL_QUEST_IDS)

        if question_ids is None:
            response = HttpResponse("Requested page not found.")
            response.status_code = HTTPStatus.NOT_FOUND
            return response

        if selected_question_progress is None:
            time_allowed = (
                len(self.request.session[MULTICHOICE_QUEST_IDS])
                * SECONDS_PER_MULTICHOIICE_QUESTION
            )
            time_allowed += (
                len(self.request.session[ESSAY_QUEST_IDS]) * SECONDS_PER_ESSAY_QUESTION
            )
            self.request.session["time_limit"] = str(
                datetime.now() + timedelta(seconds=time_allowed)
            )
        else:
            if selected_question_progress == "next":
                self.request.session[QUEST_LIST_INDEX] += 1
            elif selected_question_progress == "prev":
                self.request.session[QUEST_LIST_INDEX] -= 1

        context = self.get_context_data()
        if context[CURRENT].essay_ref is not None:
            self.form = EssayAnswerForm(request.POST)
        else:
            self.form = MultichoiceForm(request.POST)
        context["form"] = self.form
        self._get_answer()

        return render(request, self.template_name, context=context)

    def get(self, request, *args, **kwargs):
        response = HttpResponse("Method GET not allowed")
        response.status_code = HTTPStatus.METHOD_NOT_ALLOWED
        return response

    def _get_answer(self):
        if self.form is not None:
            print(self.form)
