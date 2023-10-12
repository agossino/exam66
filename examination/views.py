from django.contrib.auth.mixins import PermissionRequiredMixin
from django.views.generic import DetailView, ListView, FormView, TemplateView


from .models import MultichoiceQuestion
from .forms import MCQuestionForm


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


class MCQuestionFormView(FormView):
    template_name = "examination/form.html"
    form_class = MCQuestionForm
    success_url = "/thanks/"
