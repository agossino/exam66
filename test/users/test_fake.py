import pytest
from django.contrib.auth.models import Group, User
from examination.models import EssayQuestion, SubjectModule


# @pytest.mark.django_db
# def test_fake(new_subject_modules):
#     o = SubjectModule.objects.all()

#     for i in o:
#         print(i)

#     assert True


# @pytest.mark.django_db
# def test_random(new_essay_questions):
#     o = EssayQuestion.objects.all()

#     for i in o:
#         print(i)
#         print(i.level)
#         print(i.module)
#         print(20 * "*", SubjectModule.objects.count())

#     assert True


@pytest.mark.django_db
def test_user(new_user):
    o = User.objects.all()

    for i in o:
        print(i)
        print(20 * "*", User.objects.count())
    
    for i in Group.objects.all():
        print(i.id, i.name)

    assert True
