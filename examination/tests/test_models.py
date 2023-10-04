import re

import pytest

from examination.models import (
    EssayQuestion,
    EssayAnswer,
    MultichoiceQuestion,
    EssayQuestionUsage,
    MCQuestionUsage,
    Category,
)


@pytest.mark.django_db
class TestModels:
    def test_populate(self):
        essay_questions = EssayQuestion.objects.all()
        essay_answers = EssayAnswer.objects.all()
        mc_questions = MultichoiceQuestion.objects.all()
        essay_usages = EssayQuestionUsage.objects.all()
        mc_usages = MCQuestionUsage.objects.all()
        categories = Category.objects.all()

        assert essay_questions.count() == 3
        assert essay_answers.count() == 3
        assert mc_questions.count() == 3
        assert essay_usages.count() == 2
        assert mc_usages.count() == 2
        assert categories.count() == 11

    def test_str(self):
        date_pattern = r"\d{4}-\d{2}-\d{2}"
        essay_question = EssayQuestion.objects.get(id=1)
        essay_answer = EssayAnswer.objects.get(id=1)
        mc_question = MultichoiceQuestion.objects.get(id=1)
        category = Category.objects.get(id=1)
        mc_question_usage = MCQuestionUsage.objects.get(id=1)
        essagy_question_usage = EssayQuestionUsage.objects.get(id=1)

        assert str(essay_question) == essay_question.text
        assert essay_answer.answer[:10] in str(essay_answer)
        assert str(mc_question) == mc_question.text
        assert str(category) == category.category
        assert re.search(date_pattern, str(mc_question_usage)) is not None
        assert re.search(date_pattern, str(essagy_question_usage)) is not None

    def test_manager(self):
        valid_multichoice_questions = MultichoiceQuestion.valid_only.all()
        valid_essay_questions = EssayQuestion.valid_only.all()

        assert valid_multichoice_questions.count() == 2
        assert valid_essay_questions.count() == 2
