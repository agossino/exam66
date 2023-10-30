from django import forms


class EssayAnswerForm(forms.Form):
    answer = forms.CharField(max_length=500, strip=True)
