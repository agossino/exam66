from django.contrib import admin

from .models import (
    EssayQuestion,
    MultichoiceQuestion,
    MCQuestionUsage,
    EssayQuestionUsage,
    EssayAnswer,
    Category,
    SubjectModule,
    Chapter,
)

admin.site.register(
    [
        EssayQuestion,
        MCQuestionUsage,
        EssayQuestionUsage,
        Category,
        EssayAnswer,
        SubjectModule,
        Chapter,
    ]
)


@admin.register(MultichoiceQuestion)
class MCQuestionAdmin(admin.ModelAdmin):
    list_display = ("text", "module", "chapter", "level")
    search_fields = ("text", "module", "chapter", "level", "valid")
    date_hierarchy = "saving_time"
    ordering = ("module", "chapter", "saving_time")
