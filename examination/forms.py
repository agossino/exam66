from django import forms

from .models import MultichoiceQuestion


class MCQuestionForm(forms.ModelForm):
    class Meta:
        model = MultichoiceQuestion
        fields = "__all__"
