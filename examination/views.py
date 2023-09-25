from django.contrib.auth.decorators import permission_required, login_required
from django.views.generic import TemplateView
from django.shortcuts import get_list_or_404, render


from .models import MultichoiceQuestion


class HomeView(TemplateView):
    template_name = "examination/home.html"


@permission_required("examination.view_multichoicequestion")
# @login_required(login_url="/accounts/login/")
def list_mc_questions(request):
    questions = get_list_or_404(MultichoiceQuestion.objects.order_by("id"))
    return render(request, "examination/ls_mcquest.html", {"questions": questions})


def mdn(request):
    return render(request, "examination/mdn_structure.html")
