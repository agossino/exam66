from http import HTTPStatus

import pytest

from django.urls import reverse

from examination.models import IssuedExam


def test_home_content_block(client):
    """examination home OK"""
    url = reverse("home")
    response = client.get(url)

    assert response.status_code == HTTPStatus.OK
    assert b"Ciao from Home!" in response.content


def test_login(client):
    """Login page OK"""
    response = client.get("/accounts/login/")

    assert response.status_code == HTTPStatus.OK


@pytest.mark.django_db
def test_ls_mcquest_anonymous_user(client):
    """Anonymous user is redirected to login page."""
    url = reverse("ls_mcquest")
    response = client.get(url)

    assert response.status_code == HTTPStatus.FOUND


@pytest.mark.django_db
def test_ls_mcquest_fail_login(client):
    """ls_mcquest redirect to login page and, if it fails, username is not shown"""
    url = reverse("ls_mcquest")
    username, password = "examiner", "wrong_pw"
    client.login(username=username, password=password)
    response = client.get(url, follow=True)

    assert response.status_code == HTTPStatus.OK
    assert username.encode() not in response.content


@pytest.mark.django_db
def test_ls_mcquest_success_login(client):
    """ls_mcquest redirect to login page and, if success, username is shown"""
    url = reverse("ls_mcquest")
    username, password = "examiner", "pw"
    client.login(username=username, password=password)
    response = client.get(url, follow=True)

    assert response.status_code == HTTPStatus.OK
    assert username.encode() in response.content


@pytest.mark.django_db
def test_detail_mcquest_success_login(client):
    url = reverse("detail_mcquest", args=(1,))
    username, password = "examiner", "pw"
    client.login(username=username, password=password)
    response = client.get(url, follow=True)

    assert response.status_code == HTTPStatus.OK
    assert username.encode() in response.content


@pytest.mark.django_db
def test_detail_mcquest_fail_login(client):
    url = reverse("detail_mcquest", args=(2,))
    username, password = "examiner", "wrong_pw"
    client.login(username=username, password=password)
    response = client.get(url, follow=True)

    assert response.status_code == 200
    assert username.encode() not in response.content


@pytest.mark.django_db
def test_start_exam_anonymous_user(client):
    """Anonymous user get UNAUTHORIZED."""
    url = reverse("start_exam", args=(1,))
    response = client.get(url)

    assert response.status_code == HTTPStatus.UNAUTHORIZED


@pytest.mark.django_db
def test_start_exam_not_auth_user(client):
    """Not authorized user get UNAUTHORIZED."""
    url = reverse("start_exam", args=(1,))
    username, password = "not_authorized", "pw"
    client.login(username=username, password=password)
    response = client.get(url)

    assert response.status_code == HTTPStatus.UNAUTHORIZED


@pytest.mark.django_db
def test_start_exam_auth_user(client):
    """Authorized user get OK."""
    url = reverse("start_exam", args=(1,))
    username, password = "examiner", "pw"
    client.login(username=username, password=password)
    response = client.get(url)

    assert response.status_code == HTTPStatus.OK


@pytest.mark.django_db
def test_start_exam_check_content(client):
    """Authorized user get OK and the exam identifier."""
    exam_id = 1  # it has 2 multichoice 2 essay questions
    url = reverse("start_exam", args=(exam_id,))
    username, password = "examiner", "pw"
    client.login(username=username, password=password)
    response = client.get(url)

    assert response.status_code == HTTPStatus.OK

    exam = IssuedExam.objects.get(id=exam_id)

    assert exam.exam_tag.encode() in response.content


@pytest.mark.django_db
def test_start_exam_not_existing_exam_not_auth_user(client):
    """Not authorized user get NOT_FOUND from not existing exam id."""
    url = reverse("start_exam", args=(9999999999,))
    response = client.get(url)
    assert response.status_code == HTTPStatus.NOT_FOUND


@pytest.mark.django_db
def test_start_exam_not_existing_exam_auth_user(client):
    """Authorized user get NOT_FOUND from not existing exam id."""
    url = reverse("start_exam", args=(9999999999,))
    username, password = "user1", "pw"
    client.login(username=username, password=password)
    response = client.get(url)

    assert response.status_code == HTTPStatus.NOT_FOUND


@pytest.mark.django_db
def test_taking_exam_anonymous_user(client):
    """Anonymous user is redirected to login page."""
    url = reverse("taking_exam", args=(2,))
    response = client.get(url)

    assert response.status_code == HTTPStatus.FOUND


@pytest.mark.django_db
def test_taking_exam_get_method(client):
    """Authorized user, with taking_exam 1 arg, get GET METHOD_NOT_ALLOWED."""
    url = reverse("taking_exam", args=(2,))
    username, password = "examiner", "pw"
    client.login(username=username, password=password)
    response = client.get(url)

    assert response.status_code == HTTPStatus.METHOD_NOT_ALLOWED


@pytest.mark.django_db
def test_exam_progress_get_method(client):
    """Authorized user get GET METHOD_NOT_ALLOWED."""
    url = reverse("exam_progress", args=(1, 2))
    username, password = "examiner", "pw"
    client.login(username=username, password=password)
    response = client.get(url)

    assert response.status_code == HTTPStatus.METHOD_NOT_ALLOWED


@pytest.mark.django_db
def test_taking_exam_post_method(client):
    """Authorized user get OK."""
    url = reverse("start_exam", args=(2,))
    username, password = "user2", "pw"
    client.login(username=username, password=password)
    response = client.get(url)
    url = reverse("taking_exam", args=(2,))
    response = client.post(url)

    assert response.status_code == HTTPStatus.OK


@pytest.mark.django_db
def test_exam_progress_post_method(client):
    """Authorized user get OK."""
    url = reverse("start_exam", args=(1,))
    username, password = "user1", "pw"
    client.login(username=username, password=password)
    response = client.get(url)
    url = reverse("exam_progress", args=(1, 0))
    response = client.post(url)

    assert response.status_code == HTTPStatus.OK


@pytest.mark.django_db
def test_exam_progress_no_questions_post_method(client):
    """Authorized user trying issued exam without selected question get NOT_FOUND."""
    url = reverse("start_exam", args=(3,))
    username, password = "user3", "pw"
    client.login(username=username, password=password)
    response = client.get(url)

    response = client.get(url)
    url = reverse("exam_progress", args=(3, 0))
    response = client.post(url)

    assert response.status_code == HTTPStatus.NOT_FOUND


@pytest.mark.django_db
def test_exam_progress_next_question(client):
    """Authorized user pressing next get OK."""
    url = reverse("start_exam", args=(1,))
    username, password = "user1", "pw"
    client.login(username=username, password=password)
    response = client.get(url)

    response = client.get(url)
    url = reverse("exam_progress", args=(1, "next"))
    response = client.post(url)

    assert response.status_code == HTTPStatus.OK


@pytest.mark.django_db
def test_exam_progress_previous_question(client):
    """Authorized user pressing previuos get OK."""
    url = reverse("start_exam", args=(1,))
    username, password = "user1", "pw"
    client.login(username=username, password=password)
    response = client.get(url)

    response = client.get(url)
    url = reverse("exam_progress", args=(1, 1))
    response = client.post(url)

    response = client.get(url)
    url = reverse("exam_progress", args=(1, "prev"))
    response = client.post(url)

    assert response.status_code == HTTPStatus.OK
