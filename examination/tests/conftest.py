import pytest

from django.core.management import call_command

from django.contrib.auth.models import Permission, User

from examination.models import (
    EssayAnswer,
    GivenAnswer,
    IssuedExam,
    MultichoiceQuestion,
    SelectedQuestion,
)


@pytest.fixture(scope="session")
def django_db_setup(django_db_setup, django_db_blocker):
    """1. load data (models: SubjectModule, ChapterGroup, Chapter,
    LicenceCategory, MultichoiceQuestion, EssayQuestion, EssayAnswer);
    2. create three IssuedExam with three new Group with required permissions;
    3. select questions for IssuedExam (create SelectedQuestion
    for each selected question);
    4. create three users, join IssueExam groups to users;
    5. create examiner user and group; give it 'Can view/change
    given answer is_correct' (view will check for this permission)
    and suitable permissions for question and answer models;
    6. give one examination to eache user."""
    with django_db_blocker.unblock():
        # 1.
        call_command("loaddata", "data.json")

        # 2.
        exam_1, exam_2, exam_3 = ("First Exam", "Second Exam", "Third Exam")
        call_command("createexams", exam_1, exam_2, exam_3)

        # 3.
        issued_exam_1 = IssuedExam.objects.get(exam_tag=exam_1)
        multichoice_question_1 = MultichoiceQuestion.objects.get(id=1)
        SelectedQuestion.objects.create(
            multichoice_ref=multichoice_question_1, issued_exam=issued_exam_1
        )
        multichoice_question_3 = MultichoiceQuestion.objects.get(id=3)
        SelectedQuestion.objects.create(
            multichoice_ref=multichoice_question_3, issued_exam=issued_exam_1
        )
        essay_answer_1 = EssayAnswer.objects.get(id=1)
        SelectedQuestion.objects.create(
            essay_ref=essay_answer_1, issued_exam=issued_exam_1
        )
        essay_answer_4 = EssayAnswer.objects.get(id=4)
        SelectedQuestion.objects.create(
            essay_ref=essay_answer_4, issued_exam=issued_exam_1
        )

        issued_exam_2 = IssuedExam.objects.get(exam_tag=exam_2)
        essay_answer_2 = EssayAnswer.objects.get(id=2)
        SelectedQuestion.objects.create(
            essay_ref=essay_answer_2, issued_exam=issued_exam_2
        )

        # 4.
        username_1, username_2, username_3 = ("user1", "user2", "user3")
        pw = "pw"
        call_command(
            "createuser", username_1, pw, f"{username_1}@sciara.com", group=exam_1
        )
        call_command(
            "createuser", username_2, pw, f"{username_2}@sciara.com", group=exam_2
        )
        call_command(
            "createuser", username_3, pw, f"{username_3}@sciara.com", group=exam_3
        )

        # 5.
        call_command(
            "createuser", "examiner", "pw", "examiner0@sciara.com", group="examiners"
        )

        examiner = User.objects.get(username="examiner")
        permissions = [
            Permission.objects.get(codename=codename)
            for codename in (
                "view_multichoicequestion",
                "add_multichoicequestion",
                "change_multichoicequestion",
                "view_essayquestion",
                "add_essayquestion",
                "change_essayquestion",
                "view_essayanswer",
                "add_essayanswer",
                "change_essayanswer",
                "view_issuedexam",
                "add_issuedexam",
                "change_issuedexam",
                "view_selectedquestion",
                "add_selectedquestion",
                "change_selectedquestion",
                "view_givenanswer",
                "add_givenanswer",
                "change_givenanswer",
                "view_givenanswer_is_correct",
                "change_givenanswer_is_correct",
            )
        ]
        examiner.user_permissions.set(permissions)

        # 5.
        user = User.objects.get(username=username_1)
        selected_questions = SelectedQuestion.objects.filter(issued_exam=issued_exam_1)
        for selected_question in selected_questions:
            GivenAnswer.objects.create(
                answer="",
                is_correct=None,
                question=selected_question,
                username=user,
            )

        call_command(
            "createuser",
            "not_authorized",
            "pw",
            "not_authorized@sciara.com",
        )
