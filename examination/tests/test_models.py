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
        essay_question = EssayQuestion.objects.get(id=1)
        essay_answer = EssayAnswer.objects.get(id=1)
        mc_question = MultichoiceQuestion.objects.get(id=1)
        category = Category.objects.get(id=1)

        assert str(essay_question) == essay_question.text
        assert str(essay_answer) == essay_answer.question.text
        assert str(mc_question) == mc_question.text
        assert str(category) == category.category
