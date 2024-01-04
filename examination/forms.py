from django import forms


class EssayAnswerForm(forms.Form):
    answer = forms.CharField(max_length=500, strip=True, required=False)


class MultichoiceForm(forms.Form):
    CHOICES = [
        ("A", "Option A"),
        ("B", "Option B"),
        ("C", "Option C"),
    ]
    choice = forms.ChoiceField(
        widget=forms.RadioSelect,
        choices=CHOICES,
        required=False,
    )
