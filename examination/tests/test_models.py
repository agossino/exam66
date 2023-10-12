import re

import pytest

from examination.models import (
    EssayQuestion,
    EssayAnswer,
    MultichoiceQuestion,
    EssayQuestionUsage,
    MCQuestionUsage,
    Category,
    GivenAnswer,
    SubjectModule,
    Chapter,
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
        given_answer = GivenAnswer.objects.all()
        subject_module = SubjectModule.objects.all()
        chapter = Chapter.objects.all()

        assert essay_questions.count() == 4
        assert essay_answers.count() == 4
        assert mc_questions.count() == 4
        assert essay_usages.count() == 4
        assert mc_usages.count() == 3
        assert categories.count() == 4
        assert given_answer.count() == 2
        assert subject_module.count() == 4
        assert chapter.count() == 3

    def test_str(self):
        date_pattern = r"\d{4}-\d{2}-\d{2}"
        essay_question = EssayQuestion.objects.get(id=1)
        essay_answer = EssayAnswer.objects.get(id=1)
        mc_question = MultichoiceQuestion.objects.get(id=1)
        category = Category.objects.get(id=1)
        mc_question_usage = MCQuestionUsage.objects.get(id=1)
        essagy_question_usage = EssayQuestionUsage.objects.get(id=1)
        given_essay_anwer = GivenAnswer.objects.filter(essay_ref__isnull=False)
        given_multichoice_answer = GivenAnswer.objects.filter(
            multichoice_ref__isnull=False
        )
        subject_module = SubjectModule.objects.get(id=1)
        chapter = Chapter.objects.get(id=1)

        assert str(essay_question) == essay_question.text
        assert essay_answer.model_answer[:10] in str(essay_answer)
        assert str(mc_question) == mc_question.text
        assert str(category) == category.category
        assert re.search(date_pattern, str(mc_question_usage)) is not None
        assert re.search(date_pattern, str(essagy_question_usage)) is not None
        assert str(given_essay_anwer[0].user) in str(given_essay_anwer[0])
        assert str(given_multichoice_answer[0].user) in str(given_multichoice_answer[0])
        assert subject_module.code in str(subject_module)
        assert chapter.code in str(chapter)

    def test_manager(self):
        valid_multichoice_questions = MultichoiceQuestion.valid_only.all()
        valid_essay_questions = EssayQuestion.valid_only.all()

        assert valid_multichoice_questions.count() == 3
        assert valid_essay_questions.count() == 3
