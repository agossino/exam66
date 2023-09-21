from django.contrib import admin

from .models import (
    EssayQuestion,
    MultichoiceQuestion,
    MCQuestionUsage,
    EssayQuestionUsage,
    EssayAnswer,
    Category,
)

admin.site.register(
    [
        EssayQuestion,
        MultichoiceQuestion,
        MCQuestionUsage,
        EssayQuestionUsage,
        Category,
        EssayAnswer,
    ]
)
