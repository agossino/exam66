from django import forms
from django.contrib import admin

from .models import (
    EssayQuestion,
    MultichoiceQuestion,
    EssayAnswer,
    IssuedExam,
    SelectedQuestion,
    LicenceCategory,
    SubjectModule,
    ChapterGroup,
    Chapter,
)

admin.site.register(
    [
        EssayQuestion,
        IssuedExam,
        SelectedQuestion,
        EssayAnswer,
        SubjectModule,
        ChapterGroup,
        Chapter,
    ]
)

class LicenceCategoryForm(forms.ModelForm):
    class Meta:
        widgets = {'description': forms.TextInput(attrs={'size':'100'})}

@admin.register(LicenceCategory)
class LicenceCategoryAdmin(admin.ModelAdmin):
    form = LicenceCategoryForm


@admin.register(MultichoiceQuestion)
class MCQuestionAdmin(admin.ModelAdmin):
    list_display = ("text", "module", "chapter", "level")
    search_fields = ("text", "module", "chapter", "level", "is_valid")
    date_hierarchy = "saving_time"
    ordering = ("module", "chapter", "saving_time")
