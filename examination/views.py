from django.views.generic import TemplateView
from django.shortcuts import get_list_or_404, render

from .models import MultichoiceQuestion


class HomeView(TemplateView):
    template_name = "examination/home.html"


def view(request):
    questions = get_list_or_404(MultichoiceQuestion.objects.order_by("id"))
    return render(request, "examination/view.html", {"questions": questions})
