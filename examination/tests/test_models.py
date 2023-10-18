import pytest

from examination.models import (
    EssayQuestion,
    EssayAnswer,
    MultichoiceQuestion,
    LicenceCategory,
    IssuedExam,
    SelectedQuestion,
    GivenAnswer,
    SubjectModule,
    ChapterGroup,
    Chapter,
)


@pytest.mark.django_db
class TestModels:
    def test_populate(self):
        assert MultichoiceQuestion.objects.all().count() > 2
        assert EssayQuestion.objects.all().count() > 2
        assert EssayAnswer.objects.all().count() > 2
        assert LicenceCategory.objects.all().count() > 2
        assert IssuedExam.objects.all().count() > 2
        assert SelectedQuestion.objects.all().count() > 2
        assert GivenAnswer.objects.all().count() > 2
        assert SubjectModule.objects.all().count() > 2
        assert ChapterGroup.objects.all().count() > 2
        assert Chapter.objects.all().count() > 2

    def test_str(self):
        essay_question = EssayQuestion.objects.get(id=1)
        essay_answer = EssayAnswer.objects.get(id=1)
        mc_question = MultichoiceQuestion.objects.get(id=1)
        category = LicenceCategory.objects.get(id=1)
        issued_exam = IssuedExam.objects.get(id=1)
        selected_essay_question = SelectedQuestion.objects.filter(
            essay_ref__isnull=False
        )
        selected_given_multichoice_question = SelectedQuestion.objects.filter(
            multichoice_ref__isnull=False
        )
        given_answer = GivenAnswer.objects.get(id=1)
        subject_module = SubjectModule.objects.get(id=1)
        chapter_group = ChapterGroup.objects.get(id=1)
        chapter = Chapter.objects.get(id=1)

        assert essay_question.text in str(essay_question)
        assert essay_answer.model_answer in str(essay_answer)
        assert mc_question.text in str(mc_question)
        assert f" {category.code}" in str(category)
        assert issued_exam.exam_identifier in str(issued_exam)
        assert str(selected_essay_question[0].question) in str(
            selected_essay_question[0]
        )
        assert str(selected_given_multichoice_question[0].question) in str(
            selected_given_multichoice_question[0]
        )
        assert given_answer.answer in str(given_answer)
        assert subject_module.code in str(subject_module)
        assert chapter_group.name in str(chapter_group)
        assert chapter.code in str(chapter)

    def test_manager(self):
        valid_multichoice_questions = MultichoiceQuestion.valid_only.all()
        valid_essay_questions = EssayQuestion.valid_only.all()

        assert valid_multichoice_questions.count() == 3
        assert valid_essay_questions.count() == 3

    def test_selected_multichoice_question_save(self):
        selected_multichoice_question = SelectedQuestion.objects.create(
            multichoice_ref=MultichoiceQuestion.objects.get(id=2),
            issued_exam=IssuedExam.objects.get(id=2),
        )

        assert selected_multichoice_question.question != ""
        assert selected_multichoice_question.correct_answer != ""
        assert selected_multichoice_question.alt_answer1 != ""
        assert selected_multichoice_question.alt_answer2 != ""
        assert selected_multichoice_question.alt_answer3 != ""
        assert selected_multichoice_question.model_answer == ""

    def test_selected_essay_question_save(self):
        selected_essay_question = SelectedQuestion.objects.create(
            essay_ref=EssayAnswer.objects.get(id=2),
            issued_exam=IssuedExam.objects.get(id=2),
        )

        assert selected_essay_question.question != ""
        assert selected_essay_question.model_answer != ""
        assert selected_essay_question.key_points != ""
        assert selected_essay_question.alt_answer1 == ""
