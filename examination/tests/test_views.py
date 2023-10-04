import pytest

from django.urls import reverse


def test_home_content_block(client):
    url = reverse("home")
    response = client.get(url)

    assert response.status_code == 200
    assert b"Ciao from Home!" in response.content


def test_login(client):
    response = client.get("/accounts/login/")

    assert response.status_code == 200


@pytest.mark.django_db
def test_ls_mcquest_fail_login(client):
    url = reverse("ls_mcquest")
    username, password = "examiner0", "wrong_pw"
    client.login(username=username, password=password)
    response = client.get(url, follow=True)

    assert response.status_code == 200
    assert username.encode() not in response.content


@pytest.mark.django_db
def test_ls_mcquest_success_login(client):
    url = reverse("ls_mcquest")
    username, password = "examiner0", "pw"
    client.login(username=username, password=password)
    response = client.get(url, follow=True)

    assert response.status_code == 200
    assert username.encode() in response.content


@pytest.mark.django_db
def test_detail_mcquest_success_login(client):
    url = reverse("detail_mcquest", args=(1,))
    username, password = "examiner0", "pw"
    client.login(username=username, password=password)
    response = client.get(url, follow=True)

    assert response.status_code == 200
    assert username.encode() in response.content


@pytest.mark.django_db
def test_detail_mcquest_fail_login(client):
    url = reverse("detail_mcquest", args=(2,))
    username, password = "examiner0", "wrong_pw"
    client.login(username=username, password=password)
    response = client.get(url, follow=True)

    assert response.status_code == 200
    assert username.encode() not in response.content
